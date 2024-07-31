import { saveAs } from "file-saver";
import * as XLSX from "xlsx";

export function export_json_to_excel(headers, data, filename) {
  // 创建工作簿和工作表
  const ws = XLSX.utils.json_to_sheet(data);
  // 创建表头
  XLSX.utils.sheet_add_aoa(ws, [headers], { origin: "A1" });
  // 创建工作簿对象
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
  // 生成xlsx文件的内容
  const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
  // 创建Blob对象
  const blob = new Blob([wbout], { type: "application/octet-stream" });
  // 使用file-saver保存文件
  saveAs(blob, `${filename}.xlsx`);
}
