from django.urls import path
from system.views import viewsExcel

urlpatterns = [
    #path('admin/', admin.site.urls),

    path('excel/', viewsExcel.excel),
    path('ajaxUpload/', viewsExcel.ajaxUpload),
    path('ajaxSetTableName/', viewsExcel.ajaxSetTableName),
    path('ajaxGetTableFields/', viewsExcel.ajaxGetTableFields),
    path('ajaxSaveTableFields/', viewsExcel.ajaxSaveTableFields),
    path('excelPreviewImport/', viewsExcel.excelPreviewImport),
    path('griddata_excel_import_file_main_list/', viewsExcel.excel_import_file_main_list),
    path('griddata_excel_import_file_preview/', viewsExcel.excel_import_file_preview),
    path('ajaxExcelImport/', viewsExcel.ajaxExcelImport),
    path('excel_import_file_main_del/', viewsExcel.excel_import_file_main_del),
    path('ajaxExecSql/', viewsExcel.ajaxExecSql),

]