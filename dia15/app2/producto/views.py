# producto/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto

@login_required
def index(request):
    productos = Producto.objects.all()
    return render(request, 'productos/index.html', {'productos': productos})

@login_required
def crear(request):
    if request.method == 'POST':
        Producto.objects.create(
            codigo_barra=request.POST['codigo_barra'],
            descripcion=request.POST['descripcion'],
            precio_costo=request.POST['precio_costo'],
            precio_venta=request.POST['precio_venta'],
            iva=request.POST['iva'],
            stock=request.POST['stock'],
            unidad_medida=request.POST['unidad_medida'],
        )
    return redirect('productos_index')

@login_required
def editar(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.codigo_barra = request.POST['codigo_barra']
        producto.descripcion = request.POST['descripcion']
        producto.precio_costo = request.POST['precio_costo']
        producto.precio_venta = request.POST['precio_venta']
        producto.iva = request.POST['iva']
        producto.stock = request.POST['stock']
        producto.unidad_medida = request.POST['unidad_medida']
        producto.save()
        return redirect('productos_index')
    return render(request, 'productos/editar.html', {'producto': producto})

@login_required
def eliminar(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('productos_index')