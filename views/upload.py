from django.http import HttpResponse
from django.core.files.storage import default_storage
from datetime import datetime
from django.conf import settings
from django.utils.html import escape
import os


def upload(request):
    
    uploaded_file = request.FILES['upload']
    ck_func_num = escape(request.GET['CKEditorFuncNum'])

    date_path = datetime.now().strftime('%Y/%m/%d')    
    upload_path = os.path.join("static/upload/", date_path)
    filename = default_storage.get_available_name(os.path.join(upload_path, uploaded_file.name))
    saved_path = default_storage.save(filename, uploaded_file)

    url = default_storage.url(saved_path)

    return HttpResponse("""
    <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction({0}, '/{1}');
    </script>""".format(ck_func_num, url))