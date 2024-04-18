from typing import Any
from django.shortcuts import render, redirect
from app.models import Articulo, Comentario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, DeleteView
from .forms import ArticuloForm
# Create your views here.

class Index(ListView):
    modelo = Articulo
    queryset = Articulo.objects.all().order_by('-fecha')
    template_name = 'blog/index.html'
    paginate_by = 2
    
class Destacados(ListView):
    modelo = Articulo
    queryset = Articulo.objects.filter(destacado=True).order_by('-fecha')
    template_name = 'blog/destacados.html'
    paginate_by = 1
    
class ArticuloExtendido(DetailView):
    modelo = Articulo
    queryset = Articulo.objects.all().order_by('-fecha')
    template_name = 'blog/posteo.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticuloExtendido, self).get_context_data(*args, **kwargs)
        context['liked_by_user'] = False
        articulo = Articulo.objects.get(id=self.kwargs.get('pk'))
        if articulo.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
        context['comentarios'] = articulo.comentarios.all()
        return context
    
class ArticuloLike(View):
    def post(self, request, pk):
        articulo = Articulo.objects.get(id=pk)
        if articulo.likes.filter(pk=self.request.user.id).exists():
            articulo.likes.remove(request.user.id)
        else:
            articulo.likes.add(request.user.id)
        articulo.save
        return redirect("articulo_extendido", pk)
    
class BorrarArticulo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    modelo = Articulo
    queryset = Articulo.objects.all().order_by('-fecha')
    template_name = 'blog/borrar.html'
    success_url = reverse_lazy('inicio')
    
    def test_func(self):
        articulo = Articulo.objects.get(id=self.kwargs.get('pk'))
        return self.request.user.id == articulo.autor.id

@login_required
def agregar_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = request.user
            articulo.save()
            return redirect('inicio') 
    else:
        form = ArticuloForm()
    return render(request, 'blog/formulario.html', {'form': form})

def buscar_articulos(request):
    query = request.GET.get('busqueda')
    if query:
        articulos = Articulo.objects.filter(contenido__icontains=query)
    else:
        articulos = Articulo.objects.all()
    return render(request, 'blog/buscar_articulos.html', {'articulos': articulos, 'query': query})

@login_required
def agregar_comentario(request, pk):
    articulo = Articulo.objects.get(id=pk)
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            comentario = Comentario.objects.create(articulo=articulo, usuario=request.user, texto=texto)
            comentario.save()
    return redirect("articulo_extendido", pk=pk)

@login_required
def responder_comentario(request, pk):
    comentario_padre = Comentario.objects.get(id=pk)
    articulo = comentario_padre.articulo
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            comentario_respuesta = Comentario.objects.create(articulo=articulo, usuario=request.user, texto=texto)
            comentario_respuesta.padre = comentario_padre
            comentario_respuesta.save()
    return redirect("articulo_extendido", pk=articulo.id)

class ComentarioLike(View):
    def post(self, request, pk):
        comentario = Comentario.objects.get(id=pk)
        if comentario.likes.filter(pk=request.user.id).exists():
            comentario.likes.remove(request.user)
        else:
            comentario.likes.add(request.user)
            if comentario.dislikes.filter(pk=request.user.id).exists():
                comentario.dislikes.remove(request.user)
        comentario.save()
        return redirect("articulo_extendido", pk=comentario.articulo.id)

    
class ComentarioDislike(View):
    def post(self, request, pk):
        comentario = Comentario.objects.get(id=pk)
        if comentario.dislikes.filter(pk=request.user.id).exists():
            comentario.dislikes.remove(request.user)
        else:
            comentario.dislikes.add(request.user)
            if comentario.likes.filter(pk=request.user.id).exists():
                comentario.likes.remove(request.user)
        comentario.save()
        return redirect("articulo_extendido", pk=comentario.articulo.id)