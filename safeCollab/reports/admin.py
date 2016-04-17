from django.contrib import admin
from reports.models import Folder, HomeFolder, Report, File

class ReportAdmin(admin.ModelAdmin):
	pass

class FileAdmin(admin.ModelAdmin):
	pass

class FolderAdmin(admin.ModelAdmin):
	pass

class HomeFolderAdmin(admin.ModelAdmin):
	pass

admin.site.register(Report, ReportAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(HomeFolder, HomeFolderAdmin)