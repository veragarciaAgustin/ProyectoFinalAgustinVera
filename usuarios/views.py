from django.shortcuts import render, redirect
from django.views import View
from .forms import FormularioRegistro
from django.contrib.auth import logout

# Create your views here.

class Registrarse(View):
    def get(self, request):
        form = FormularioRegistro()
        return render(request, "usuarios/registro.html", {'form': form})
    
    def post(self, request):
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            form.save()
            # Asegura que la redirección se hace correctamente
            return redirect('login') 
        else:
            # Si el formulario no es válido, renderiza de nuevo la página con el formulario y errores
            return render(request, "usuarios/registro.html", {'form': form})
        
def logout_view(request):
    logout(request)
    return render(request, "usuarios/logout.html")