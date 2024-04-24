from django.contrib import admin
import appcaulie.models as am

# Register your models here.


class GeneinfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'chromosome', 'start', 'end', 'strand')
    list_filter = ('chromosome', 'strand')
    search_fields = ('id', 'chromosome')
    list_per_page = 40


class SampleinfoAdmin(admin.ModelAdmin):
    list_display = ('sampleid', 'name', 'clade', 'group', 'taxonomy')
    list_filter = ('name', 'clade', 'taxonomy')
    search_fields = ('sampleid', 'name', 'clade')
    list_per_page = 40


admin.site.register(am.Geneinfo, GeneinfoAdmin)
admin.site.register(am.Sampleinfo, SampleinfoAdmin)