const URL_BASE = "http://127.0.0.1:5000/api";

// Función para actualizar las métricas clave (Metric Cards)
async function actualizarMetricas() {
  const metProductosVal = document.getElementById("met-productos-valor");
  const metCarritoVal = document.getElementById("met-carrito-valor");

  try {
    // Obtener total productos
    const resProd = await fetch(`${URL_BASE}/productos`);
    const productos = await resProd.json();
    metProductosVal.textContent = productos.length;

    // Obtener total artículos distintos en carrito
    const resCarrito = await fetch(`${URL_BASE}/carrito`);
    const items = await resCarrito.json();
    metCarritoVal.textContent = items.length; // Número de productos distintos
  } catch (err) {
    console.error("Error actualizando métricas", err);
  }
}

// Al cargar la página, inicializa la tienda y las métricas
document.addEventListener("DOMContentLoaded", () => {
  actualizarMetricas();
  cargarProductos();
  cargarCategorias();
  actualizarVistaCarrito();
});

// REQUISITO 1: Ver todos los productos (u opcionalmente por categoría) - REDISEÑADO
async function cargarProductos(categoria = "TODOS") {
  const contenedor = document.getElementById("lista-productos");
  contenedor.innerHTML =
    '<p style="grid-column: 1 / -1; text-align: center;">Cargando inventario local...</p>';

  let url = `${URL_BASE}/productos`;
  if (categoria !== "TODOS") {
    url = `${URL_BASE}/productos/categoria/${categoria}`;
  }

  try {
    const res = await fetch(url);
    const productos = await res.json();
    contenedor.innerHTML = "";

    if (productos.length === 0) {
      contenedor.innerHTML =
        '<p style="grid-column: 1 / -1; text-align: center;">No hay artículos disponibles en esta sección.</p>';
      return;
    }

    productos.forEach((p) => {
      const card = document.createElement("div");
      card.className = "card-producto-dashboard";
      card.innerHTML = `
                <div>
                    <h3>${p.nombre}</h3>
                    <p style="font-size:13px; color:#9ca3af;">${p.descripcion || ""}</p>
                    <p class="precio-dashboard">$${p.precio.toFixed(2)}</p>
                    <span class="status-tag tag-stock">Disponibles: ${p.stock}</span>
                </div>
                <div class="buy-controls-dashboard">
                    <input type="number" id="cant-${p.id}" value="1" min="1" max="${p.stock}">
                    <button onclick="agregarArticulo('${p.id}')">Agregar</button>
                </div>
            `;
      contenedor.appendChild(card);
    });
  } catch (err) {
    contenedor.innerHTML =
      '<p style="grid-column: 1 / -1; text-align: center; color:red;">❌ Error al conectar con el backend.</p>';
  }
}

// REQUISITO 2: Buscar productos por Categoría (Llena el desplegable) - REDISEÑADO
async function cargarCategorias() {
  const combo = document.getElementById("combo-categorias");
  try {
    const res = await fetch(`${URL_BASE}/categorias`);
    const categorias = await res.json();

    categorias.forEach((cat) => {
      const opt = document.createElement("option");
      opt.value = cat;
      opt.textContent = cat.toUpperCase();
      combo.appendChild(opt);
    });
  } catch (err) {
    console.error("Error cargando categorías", err);
  }
}

function cambiarCategoria() {
  const seleccionada = document.getElementById("combo-categorias").value;
  cargarProductos(seleccionada);
}

// REQUISITO 3: Agregar producto al carrito
async function agregarArticulo(productoId) {
  const inputCantidad = document.getElementById(`cant-${productoId}`);
  const cantidad = parseInt(inputCantidad.value) || 1;

  try {
    const res = await fetch(`${URL_BASE}/carrito/agregar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ producto_id: productoId, cantidad: cantidad }),
    });
    const data = await res.json();

    // No mostramos alerta aquí para no interrumpir, solo actualizamos vista
    console.log(data.mensaje);
    actualizarVistaCarrito();
  } catch (err) {
    alert("No se pudo agregar el producto.");
  }
}

// REQUISITO 4: Ver el contenido del carrito - REDISEÑADO
async function actualizarVistaCarrito() {
  const contenedor = document.getElementById("contenido-carrito");
  const txtTotal = document.getElementById("total-precio");

  try {
    const res = await fetch(`${URL_BASE}/carrito`);
    const items = await res.json();
    contenedor.innerHTML = "";
    let totalAcumulado = 0;

    if (items.length === 0) {
      contenedor.innerHTML =
        '<p style="color:#6b7280; text-align:center;">El carrito está vacío.</p>';
      txtTotal.textContent = "0.00";
      actualizarMetricas();
      return;
    }

    items.forEach((item) => {
      totalAcumulado += item.subtotal;
      const divItem = document.createElement("div");
      divItem.className = "detailed-cart-item";
      divItem.innerHTML = `
                <span><strong>${item.nombre}</strong> (x${item.cantidad})</span>
                <span>$${item.subtotal.toFixed(2)}</span>
            `;
      contenedor.appendChild(divItem);
    });

    txtTotal.textContent = totalAcumulado.toFixed(2);
  } catch (err) {
    contenedor.innerHTML =
      '<p style="color:red;">Error al leer el carrito.</p>';
  }

  // Actualizamos las métricas cada vez que cambia el carrito
  actualizarMetricas();
}

// REQUISITO 5: Realizar la compra (Descuenta inventario en MongoDB)
async function procesarPago() {
  if (!confirm("¿Confirmas que deseas finalizar tu compra?")) return;

  try {
    const res = await fetch(`${URL_BASE}/carrito/comprar`, { method: "POST" });
    const data = await res.json();

    alert(data.mensaje);

    // Refrescamos los componentes para ver el stock actualizado inmediatamente
    actualizarMetricas();
    actualizarVistaCarrito();
    cambiarCategoria();
  } catch (err) {
    alert("Ocurrió un error al procesar el checkout.");
  }
}
