from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from jobs.models import Client, DevelopmentSite, Job


class DevelopmentSiteInline(admin.TabularInline):
    model = DevelopmentSite


class JobInline(admin.TabularInline):
    model = Job


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    def num_sites(self, instance):
        return instance.num_sites

    # List of instances
    list_display = ('name', 'part_code', 'num_sites', )
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    
    inlines = [DevelopmentSiteInline]


@admin.register(DevelopmentSite)
class DevelopmentSiteAdmin(admin.ModelAdmin):
    def full_code(self, instance):
        return instance.full_code

    def num_jobs(self, instance):
        return instance.num_jobs

    # List of instances
    list_display = ('client', 'name', 'full_code', 'num_jobs', )
    list_display_links = ('name',)
    list_filter = ('client', 'name',)
    search_fields = ('client', 'name',)
    ordering = ('client', 'name',)
    
    inlines = [JobInline]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    def client(self, instance):
        return instance.client

    # List of instances
    list_display = ('client', 'site', 'plot_number', 'tenure', 'full_code')
    list_display_links = ('plot_number',)
    list_filter = ('site', 'tenure',)
    search_fields = ('site', 'plot_number',)
    ordering = ('site', 'plot_number',)
