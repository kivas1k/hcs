from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from appeals.models import Appeal, Tag
from users.models import User
import pandas as pd
from io import BytesIO
from datetime import datetime


class ReportsView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['staff', 'admin']

    def get(self, request):
        context = self.get_base_context()
        return render(request, 'reports/reports.html', context)

    def post(self, request):
        context = self.get_base_context()
        params = self.get_filter_params(request)

        queryset = Appeal.objects.all()
        queryset = self.apply_filters(queryset, params)

        if 'export' in request.POST:
            return self.export_to_excel(queryset)

        context['report_data'] = self.prepare_report_data(queryset)
        return render(request, 'reports/reports.html', context)

    def get_base_context(self):
        return {
            'status_choices': Appeal.STATUS_CHOICES,
            'priority_choices': Appeal.PRIORITY_CHOICES,
            'employees': User.objects.filter(role__in=['staff', 'admin']),
            'tags': Tag.objects.all(),
            'authors': User.objects.filter(appeals__isnull=False).distinct(),
        }

    def get_filter_params(self, request):
        return {
            'status': request.POST.get('status'),
            'priority': request.POST.get('priority'),
            'tag': request.POST.get('tag'),
            'employee': request.POST.get('employee'),
            'author': request.POST.get('author'),
            'start_date': request.POST.get('start_date'),
            'end_date': request.POST.get('end_date'),
        }

    def apply_filters(self, queryset, params):
        if params['status']:
            queryset = queryset.filter(status=params['status'])
        if params['priority']:
            queryset = queryset.filter(priority=params['priority'])
        if params['tag']:
            queryset = queryset.filter(tags__id=params['tag'])
        if params['author']:
            queryset = queryset.filter(author_id=params['author'])
        if params['employee'] and self.request.user.role == 'admin':
            queryset = queryset.filter(taken_by_id=params['employee'])
        if params['start_date'] and params['end_date']:
            try:
                start_date = datetime.strptime(params['start_date'], '%Y-%m-%d')
                end_date = datetime.strptime(params['end_date'], '%Y-%m-%d')
                start_date = timezone.make_aware(start_date)
                end_date = timezone.make_aware(end_date)
                queryset = queryset.filter(created_at__range=(start_date, end_date))
            except ValueError:
                pass
        return queryset

    def prepare_report_data(self, queryset):
        return [{
            'ID': appeal.id,
            'Заголовок': appeal.title,
            'Статус': appeal.get_status_display(),
            'Приоритет': appeal.get_priority_display(),
            'Автор': appeal.author.username,
            'Дата_создания': appeal.created_at.strftime('%d.%m.%Y %H:%M'),
            'Теги': ', '.join([tag.name for tag in appeal.tags.all()]),
            'Исполнитель': appeal.taken_by.username if appeal.taken_by else '-',
        } for appeal in queryset]

    def export_to_excel(self, queryset):
        # Подготовка данных
        data = self.prepare_report_data(queryset)
        columns = {
            'ID': 'ID',
            'Заголовок': 'Заголовок',
            'Статус': 'Статус',
            'Приоритет': 'Приоритет',
            'Автор': 'Автор',
            'Дата_создания': 'Дата создания',
            'Теги': 'Теги',
            'Исполнитель': 'Исполнитель'
        }

        df = pd.DataFrame(data).rename(columns=columns)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Отчет')
            worksheet = writer.sheets['Отчет']

            for idx, col in enumerate(df.columns):
                max_len = max(
                    df[col].astype(str).map(len).max(),
                    len(col)
                ) + 1
                worksheet.set_column(idx, idx, min(max_len, 30))

        output.seek(0)
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=report.xlsx'
        return response