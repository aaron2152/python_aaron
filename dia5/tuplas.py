sucursal_a = (-25.2637,-57.5759)
sucursal_b = (-25.2968,-57.6350)

lat_a, lon_a = sucursal_a
lat_b, lon_b = sucursal_b
distancia = ((lat_b - lat_a)**2 + (lon_b - lon_a)**2)**0.5
print(f"La distancia entre sucursales es: {distancia:.4f} grados")
