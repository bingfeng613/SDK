import io
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

from .models import App
from .serializers import AppSerializer, UserLoginSerializer, PasswordChangeSerializer, UserRegistrationSerializer


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

# 账号
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_info = serializer.validated_data
            user = user_info.get('user')
            if user:
                return Response({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'account': user.account,
                    }
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

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
# todo：接文件上传腾讯云
class AppUploadView(APIView): # 未接文本解析，上传后增加默认记录
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        if not files:
            return Response({'error': 'No files provided.'}, status=400)

        for file in files:
            app = App(
                appName='test appName',
                lackDataNum=0,
                fuzzyDataNum=0,
                brokenLinkNum=0,
                lackData='test lackData',
                fuzzyData='test fuzzyData',
                brokenLink='test brokenLink',
                htmlUrl='http://f0.0sm.com/node0/2024/08/866ACE1765AB52F8-d8dc519c7d5ac198.jpg' # 默认固定文件Url
            )
            app.save()

        return Response({'message': f'{len(files)} files uploaded successfully.'}, status=201)

# 已解析库
class AppListView(generics.ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    pagination_class = CustomPageNumberPagination

class AppSearchView(generics.ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('keyword', None)
        if keyword:
            queryset = queryset.filter(Q(appName__icontains=keyword))
        return queryset

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
        # data = JSONParser().parse(request)
        #
        # app_ids = data.get('ids')
        # json or raw？
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
# 返回固定数据
# todo:填完数据库后，加上计算逻辑
class StatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        ids = request.query_params.getlist('ids')
        if ids:
            # filtered_data = self.filter_data_by_ids(ids)
            # 计算逻辑
            pass
        else:
            return Response({'error': 'ids must be provided'}, status=400)

        data = {
            "appNum": 30,
            "declareGroupNum": 618,
            "declareUrlNum": 315,
            "complianceGroupNum": 278,
            "complianceGroupProportion": "45%",
            "lackDataNum": 185,
            "lackDataProportion": "30%",
            "fuzzyDataNum": 155,
            "fuzzyDataProportion": "25%",
            "complianceUrlNum": 95,
            "complianceUrlProportion": "30%",
            "UnableToConnectNum": 15,
            "UnableToConnectProportion": "5%",
            "NotPrivacyPolicyNum": 110,
            "NotPrivacyPolicyProportion": "35%",
            "appPrivacyPolicyNum": 47,
            "appPrivacyPolicyProportion": "15%",
            "notDataInsidePrivacyPolicyNum": 48,
            "notDataInsidePrivacyPolicyProportion": "15%"
        }
        return Response(data, status=status.HTTP_200_OK)

    def filter_data_by_ids(self, ids):
        pass


class StatisticsExcelView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "appNum": 30,
            "declareGroupNum": 618,
            "declareUrlNum": 315,
            "complianceGroupNum": 278,
            "complianceGroupProportion": "45%",
            "lackDataNum": 185,
            "lackDataProportion": "30%",
            "fuzzyDataNum": 155,
            "fuzzyDataProportion": "25%",
            "complianceUrlNum": 95,
            "complianceUrlProportion": "30%",
            "UnableToConnectNum": 15,
            "UnableToConnectProportion": "5%",
            "NotPrivacyPolicyNum": 110,
            "NotPrivacyPolicyProportion": "35%",
            "appPrivacyPolicyNum": 47,
            "appPrivacyPolicyProportion": "15%",
            "notDataInsidePrivacyPolicyNum": 48,
            "notDataInsidePrivacyPolicyProportion": "15%"
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