from django.urls import path, include
from .views import Index, ArticuloExtendido, ArticuloLike, Destacados, BorrarArticulo, ComentarioLike, ComentarioDislike
from . import views

urlpatterns = [
    path('', Index.as_view(), name="inicio"),
    path('tinymce/', include('tinymce.urls')),
    path('<int:pk>/', ArticuloExtendido.as_view(), name='articulo_extendido'),
    path('<int:pk>/like', ArticuloLike.as_view(), name='articulo_like' ),
    path('destacados/', Destacados.as_view(), name='destacados'),
    path('<int:pk>/borrar', BorrarArticulo.as_view(), name='borrar_articulo' ),
    path('agregar/', views.agregar_articulo, name='agregar_articulo'),
    path('buscar/', views.buscar_articulos, name='buscar_articulos'),
    path('<int:pk>/comentar/', views.agregar_comentario, name='agregar_comentario'),
    path('<int:pk>/responder/', views.responder_comentario, name='responder_comentario'),
    path('comentario/<int:pk>/like/', ComentarioLike.as_view(), name='comentario_like'),
     path('<int:pk>/dislike/', ComentarioDislike.as_view(), name='comentario_dislike'),
]
