"""
URL configuration for projeto_imoveis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views as api_views # Importa nossas views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpoints da API
    path('api/evolucao-ano/', api_views.get_evolucao_por_ano),
    path('api/preco-bairro/', api_views.get_preco_por_bairro),
    path('api/filtrar/', api_views.get_dados_filtrados),
]