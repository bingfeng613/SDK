import io
import json
import os
import zipfile

import xlsxwriter
import requests
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.db.models.functions import datetime
from django.http import FileResponse, HttpResponse
from rest_framework import generics, pagination, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from xlsxwriter import Workbook
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from .models import App, User, MyCosConfig
from .serializers import AppSerializer, UserRegistrationSerializer, PasswordChangeSerializer, UserLoginSerializer


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

# 账号
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_info = serializer.validated_data
            return Response({
                'account': user_info,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            print(serializer.validated_data)
            account = serializer.validated_data.get('account')
            user = User.objects.get(account=account)
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response({
                'message': '密码修改成功',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'account': user.account,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 上传文件
# todo：接文本解析框架
class AppUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        if not files:
            return Response({'error': 'No files provided.'}, status=400)

        account = request.data.get('account')
        if not account:
            return Response({'error': 'Account parameter is required.'}, status=400)

        cos_config = MyCosConfig.objects.first()
        if not cos_config:
            return Response({'error': 'CosConfig not found.'}, status=400)

        config = CosConfig(Region=cos_config.region, SecretId=cos_config.secret_id, SecretKey=cos_config.secret_key)
        client = CosS3Client(config)

        for file in files:
            response = client.put_object(
                Bucket=cos_config.bucket_name,
                Body=file,
                Key=file.name,
                StorageClass='STANDARD',
                ACL='public-read',
                CacheControl='max-age=3600'
            )

            file_url = f"https://{cos_config.bucket_name}.cos.{cos_config.region}.myqcloud.com/{file.name}"

            app = App(
                appName='test appName',
                account=account,
                totalDataNum=10,
                totalUrlNum=10,
                lackDataNum=1,
                fuzzyDataNum=2,
                brokenLinkNum=6,
                lackData='test lackData',
                fuzzyData='test fuzzyData',
                UnableToConnectNum=1,
                NotPrivacyPolicyNum=2,
                appPrivacyPolicyNum=1,
                notDataInsidePrivacyPolicyNum=2,
                UnableToConnectLink='test UnableToConnectLink',
                NotPrivacyPolicyLink='test NotPrivacyPolicyLink',
                appPrivacyPolicyLink='test appPrivacyPolicyLink',
                notDataInsidePrivacyPolicyLink='test notDataInsidePrivacyPolicyLink',
                brokenLink='test brokenLink',
                htmlUrl=file_url
            )
            app.save()

        return Response({'message': f'{len(files)} files uploaded successfully.'}, status=201)



# 已解析库
class AppListView(generics.ListAPIView):
    # queryset = App.objects.all()
    serializer_class = AppSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        account = self.request.query_params.get('account', None)
        if account is not None:
            return App.objects.filter(account=account)
        else:
            return Response({'error': 'Account parameter is required.'}, status=400)

class AppSearchView(generics.ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        account = self.request.query_params.get('account', None)
        if account is not None:
            all_set=App.objects.filter(account=account)
            keyword = self.request.query_params.get('keyword', None)
            if keyword:
                queryset = all_set.filter(Q(appName__icontains=keyword))
            return queryset
        else:
            return Response({'error': 'Account parameter is required.'}, status=400)


class AppDeleteView(generics.GenericAPIView):
    def delete(self, request, *args, **kwargs):
        app_ids = request.data.get('ids')
        if app_ids and isinstance(app_ids, list):
            try:
                app_ids = [int(id_str) for id_str in app_ids]
                App.objects.filter(id__in=app_ids).delete()
                return Response({'message': 'Selected apps deleted successfully'}, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Invalid IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'IDs must be a list of integers'}, status=status.HTTP_400_BAD_REQUEST)

class AppExcelView(APIView):
    def post(self, request, *args, **kwargs):
        app_ids = request.data.get('ids')

        if app_ids:
            try:
                apps = App.objects.filter(id__in=app_ids)
                serializer = AppSerializer(apps, many=True)
                response_data = serializer.data

                output = io.BytesIO()
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()

                headers = response_data[0].keys()
                for col, header in enumerate(headers):
                    worksheet.write(0, col, header)

                for row_idx, app_data in enumerate(response_data):
                    for col, cell_data in enumerate(app_data.values()):
                        worksheet.write(row_idx + 1, col, cell_data)

                workbook.close()
                filename = 'apps_export_{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
                output.seek(0)

                return FileResponse(output, as_attachment=True, filename=filename)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        else:
            return Response({'error': 'IDs must be provided'}, status=400)

class AppDownloadView(APIView):
    def post(self, request, *args, **kwargs):
        app_ids = request.data.get('ids')

        if not app_ids:
            return Response({'error': 'No app ids provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # 准备存储下载文件的目录
        temp_dir = '/tmp/app_downloads'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # 下载文件并存储到临时目录
        downloaded_files = []
        for app_id in app_ids:
            try:
                app_record = App.objects.get(id=app_id)
                url = app_record.htmlUrl
                response = requests.get(url)

                if response.status_code == 200:
                    file_name = os.path.basename(url)
                    file_path = os.path.join(temp_dir, file_name)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    downloaded_files.append(file_path)
                else:
                    return Response({'error': f'Failed to download file for app id {app_id}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except App.DoesNotExist:
                return Response({'error': f'App with id {app_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            except requests.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 准备ZIP响应
        if downloaded_files:
            zip_file_path = os.path.join(temp_dir, 'downloads.zip')
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for file_path in downloaded_files:
                    zipf.write(file_path, os.path.basename(file_path))

            # 发送ZIP文件作为HTTP响应
            with open(zip_file_path, 'rb') as f:
                response = HttpResponse(f, content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="downloads.zip"'
                return response

            # 清理临时文件
            for file_path in downloaded_files:
                os.remove(file_path)
            os.remove(zip_file_path)
            os.rmdir(temp_dir)

        return Response({'error': 'No files to download.'}, status=status.HTTP_404_NOT_FOUND)

# 统计数据
class StatisticsView(APIView):
    def get(self, request, *args, **kwargs):

        ids_str = request.query_params.get('ids')
        if ids_str:
            try:
                ids = json.loads(ids_str)
                if not isinstance(ids, list):
                    raise ValueError("ids parameter is not a list")
            except json.JSONDecodeError:
                return Response({'error': 'ids parameter is not valid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'ids must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_records = App.objects.filter(id__in=ids)
        except App.DoesNotExist:
            return Response({'error': 'One or more ids are not found'}, status=status.HTTP_404_NOT_FOUND)

        print(type(data_records))

        total_app_num = len(ids)
        total_declare_group_num = sum(item.totalDataNum for item in data_records)
        total_declare_url_num = sum(item.totalUrlNum for item in data_records)

        total_lack_data_num = sum(item.lackDataNum for item in data_records)
        total_fuzzy_data_num = sum(item.fuzzyDataNum for item in data_records)
        total_compliance_group_num = total_declare_group_num-total_lack_data_num-total_fuzzy_data_num

        total_unableToConnect_num = sum(item.UnableToConnectNum for item in data_records)
        total_notPrivacyPolicy_num = sum(item.NotPrivacyPolicyNum for item in data_records)
        total_appPrivacyPolicy_num = sum(item.appPrivacyPolicyNum for item in data_records)
        total_notDataInsidePrivacyPolicy_num = sum(item.notDataInsidePrivacyPolicyNum for item in data_records)
        total_compliance_url_num = total_declare_url_num-total_unableToConnect_num-total_notPrivacyPolicy_num-total_appPrivacyPolicy_num-total_notDataInsidePrivacyPolicy_num

        print(total_lack_data_num, total_fuzzy_data_num, total_app_num)


        data = {
            "appNum": total_app_num,
            "declareGroupNum": total_declare_group_num,
            "declareUrlNum": total_declare_url_num,

            "complianceGroupNum": total_compliance_group_num,
            "complianceGroupProportion": f"{round(total_compliance_group_num / total_declare_group_num* 100, 2)}%",
            "lackDataNum": total_lack_data_num,
            "lackDataProportion": f"{round(total_lack_data_num / total_declare_group_num* 100, 2)}%",
            "fuzzyDataNum": total_fuzzy_data_num,
            "fuzzyDataProportion": f"{round(total_fuzzy_data_num / total_declare_group_num* 100, 2)}%",

            "complianceUrlNum": total_compliance_url_num,
            "complianceUrlProportion": f"{round(total_compliance_url_num / total_declare_url_num* 100, 2)}%",
            "UnableToConnectNum": total_unableToConnect_num,
            "UnableToConnectProportion": f"{round(total_unableToConnect_num / total_declare_url_num* 100, 2)}%",
            "NotPrivacyPolicyNum": total_notPrivacyPolicy_num,
            "NotPrivacyPolicyProportion": f"{round(total_notPrivacyPolicy_num / total_declare_url_num* 100, 2)}%",
            "appPrivacyPolicyNum": total_appPrivacyPolicy_num,
            "appPrivacyPolicyProportion": f"{round(total_appPrivacyPolicy_num / total_declare_url_num* 100, 2)}%",
            "notDataInsidePrivacyPolicyNum": total_notDataInsidePrivacyPolicy_num,
            "notDataInsidePrivacyPolicyProportion": f"{round(total_notDataInsidePrivacyPolicy_num / total_declare_url_num* 100, 2)}%",
        }
        return Response(data, status=status.HTTP_200_OK)

    def filter_data_by_ids(self, ids):
        pass


class StatisticsExcelView(APIView):
    def get(self, request, *args, **kwargs):

        ids_str = request.query_params.get('ids')
        if ids_str:
            try:
                ids = json.loads(ids_str)
                if not isinstance(ids, list):
                    raise ValueError("ids parameter is not a list")
            except json.JSONDecodeError:
                return Response({'error': 'ids parameter is not valid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'ids must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_records = App.objects.filter(id__in=ids)
        except App.DoesNotExist:
            return Response({'error': 'One or more ids are not found'}, status=status.HTTP_404_NOT_FOUND)

        print(type(data_records))

        total_app_num = len(ids)
        total_declare_group_num = sum(item.totalDataNum for item in data_records)
        total_declare_url_num = sum(item.totalUrlNum for item in data_records)

        total_lack_data_num = sum(item.lackDataNum for item in data_records)
        total_fuzzy_data_num = sum(item.fuzzyDataNum for item in data_records)
        total_compliance_group_num = total_declare_group_num - total_lack_data_num - total_fuzzy_data_num

        total_unableToConnect_num = sum(item.UnableToConnectNum for item in data_records)
        total_notPrivacyPolicy_num = sum(item.NotPrivacyPolicyNum for item in data_records)
        total_appPrivacyPolicy_num = sum(item.appPrivacyPolicyNum for item in data_records)
        total_notDataInsidePrivacyPolicy_num = sum(item.notDataInsidePrivacyPolicyNum for item in data_records)
        total_compliance_url_num = total_declare_url_num - total_unableToConnect_num - total_notPrivacyPolicy_num - total_appPrivacyPolicy_num - total_notDataInsidePrivacyPolicy_num

        print(total_lack_data_num, total_fuzzy_data_num, total_app_num)

        data = {
            "appNum": total_app_num,
            "declareGroupNum": total_declare_group_num,
            "declareUrlNum": total_declare_url_num,

            "complianceGroupNum": total_compliance_group_num,
            "complianceGroupProportion": f"{round(total_compliance_group_num / total_declare_group_num * 100, 2)}%",
            "lackDataNum": total_lack_data_num,
            "lackDataProportion": f"{round(total_lack_data_num / total_declare_group_num * 100, 2)}%",
            "fuzzyDataNum": total_fuzzy_data_num,
            "fuzzyDataProportion": f"{round(total_fuzzy_data_num / total_declare_group_num * 100, 2)}%",

            "complianceUrlNum": total_compliance_url_num,
            "complianceUrlProportion": f"{round(total_compliance_url_num / total_declare_url_num * 100, 2)}%",
            "UnableToConnectNum": total_unableToConnect_num,
            "UnableToConnectProportion": f"{round(total_unableToConnect_num / total_declare_url_num * 100, 2)}%",
            "NotPrivacyPolicyNum": total_notPrivacyPolicy_num,
            "NotPrivacyPolicyProportion": f"{round(total_notPrivacyPolicy_num / total_declare_url_num * 100, 2)}%",
            "appPrivacyPolicyNum": total_appPrivacyPolicy_num,
            "appPrivacyPolicyProportion": f"{round(total_appPrivacyPolicy_num / total_declare_url_num * 100, 2)}%",
            "notDataInsidePrivacyPolicyNum": total_notDataInsidePrivacyPolicy_num,
            "notDataInsidePrivacyPolicyProportion": f"{round(total_notDataInsidePrivacyPolicy_num / total_declare_url_num * 100, 2)}%",
        }

        # 创建一个内存中的IO对象
        output = io.BytesIO()
        workbook = Workbook(output)
        worksheet = workbook.add_worksheet()

        titles = ['Statistic', 'Value']
        for i, title in enumerate(titles):
            worksheet.write(0, i, title)

        row = 1
        for key, value in data.items():
            worksheet.write(row, 0, key)
            worksheet.write(row, 1, value)
            row += 1

        workbook.close()

        # 重置output指针到开始位置
        output.seek(0)

        # 构造文件响应
        return FileResponse(output, as_attachment=True, filename='statistics.xlsx')