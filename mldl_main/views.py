from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .predict_DL import predict_cnn_one
from .recommend_system import recommend_recipe_list
import pandas as pd
import pickle

# Create your views here.

def index(request):
    return render(request, 'mldl_main/index.html', {})


def dl_cnn(request):
    return render(request, 'mldl_main/dl_cnn.html', {})


def predict_cnn(request):

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    uploaded_file = request.FILES['img_uploaded']
    fs = FileSystemStorage()
    uploaded_filename = fs.save(uploaded_file.name, uploaded_file)
    uploaded_file_url = fs.url(uploaded_filename) # "/media/~~~.jpg"

    predict_result = predict_cnn_one(settings.MEDIA_ROOT_URL + uploaded_file_url)

    df =  pd.read_excel(base_url + 'save_ingredient_DB.xlsx', index_col = 0)
    save_ingredient_list = df['Name'].values.tolist()
    save_ingredient_list.append(predict_result)
    df = pd.DataFrame(save_ingredient_list, columns=['Name'])
    df.to_excel(base_url + 'save_ingredient_DB.xlsx')

    context = {'uploaded_file_url':uploaded_file_url,
               'uploaded_file_name':uploaded_filename,
               'predict_result' : predict_result,
               'save_ingredient_list' : save_ingredient_list}

    return render(request, 'mldl_main/dl_cnn_result.html', context)


def delete_cnn(request, file_name):

    fs = FileSystemStorage()
    fs.delete(file_name)

    return redirect('mldl_main:index')


def recommend_recipe(request):

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    df =  pd.read_excel(base_url + 'save_ingredient_DB.xlsx', index_col = 0)
    save_ingredient_list = df['Name'].values.tolist()
    recommend_recipe_result = recommend_recipe_list(save_ingredient_list)

    context = {'recommend_recipe_result':recommend_recipe_result.to_html()}

    return render(request, 'mldl_main/recommend.html', context )



def recommend_delete(request):

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    df = pd.DataFrame(columns=['Name'])
    df.to_excel(base_url + 'save_ingredient_DB.xlsx')

    return redirect('mldl_main:index')
