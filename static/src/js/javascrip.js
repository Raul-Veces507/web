$(document).ready(function () {
  $(".add-to-cart-button").click(function () {
    // var addToCartUrl = window.addToCartUrl;
    // console.log(window.addToCartUrl);

    var product_id = $(this).data("product-id");
    var urlfinal = addToCartUrl.replace('0', product_id)
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: urlfinal,
      method: "POST",
      dataType: "json",
      headers: {
        "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
      },
      success: function (data) {

        if (data.status === "success") {
          fetch(cartoCartUrl)
            .then(response => response.json())
            .then(cartData => {
              var toast = document.getElementById("toast");
              toast.style.display = "block";
              setTimeout(function () {
                toast.style.display = "none";
              }, 1500);

              var cartCountElement = document.getElementById("cart-count");
              if (cartCountElement) {
                cartCountElement.textContent = cartData.cart_count;
              }
            })
            .catch(error => {
              console.error("Error al obtener la cantidad del carrito", error);
            });
          // Actualiza la interfaz de usuario según sea necesario
        } else if (data.status == 'carrito') {
          window.location.href = carrito
          var toast = document.getElementById("toast");
          toast.style.display = "block";
          setTimeout(function () {
            toast.style.display = "none";
          }, 1500);

          var cartCountElement = document.getElementById("cart-count");
          if (cartCountElement) {
            cartCountElement.textContent = cartData.cart_count;
          }

        } else {
          alert("Error al agregar el producto al carrito");
        }
      }
    })
  })



  ////eliminar Productos del carrito


  function carritomodal(){
    fetch(vercarrito)
    .then(response => response.json())
    .then(cartData => {

      if (cartData['cart_items'] == '' ||cartData['cart_items'] == undefined ) {
        window.location.href = carrito;
      } else {
        modalcarrito.style.display = (modalcarrito.style.display === 'none') ? 'block' : 'none';
        var datos = cartData['cart_items'];
        // console.log(datos);
        var dato2 = Number(cartData['total'])


        var resultsHtml = '     <div class="flow-root">';
        resultsHtml += '       <ul role="list" class="-my-6 divide-y divide-gray-200">';
        datos.forEach(function (data) {
          resultsHtml += '         <li class="flex py-6">';
          resultsHtml += '           <div style="    width: 120px; height: 120px;" class="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">';
          resultsHtml += ` <img src="https://riba.app/imgrs/THUMBS 500X500/${data.item}.jpg" alt="not found class="w-full h-full object-cover object-center" onerror="this.src='https://www.ribasmith.com/media/catalog/product/placeholder/default/watermark_4.png' ">`;
          resultsHtml += '           </div>';
          resultsHtml += '           <div class="ml-5 flex flex-1 flex-col">';
          resultsHtml += '             <div>';
          resultsHtml += '               <div class="flex justify-between text-base font-medium text-gray-900">';
          resultsHtml += '                 <h3>';
          resultsHtml += `                   <a href="#">${data.nombre.slice (0, 12)}...</a>`;
          resultsHtml += '                 </h3>';
          resultsHtml += `                <p class="ml-4 text-indigo-600">$ ${data.total.toFixed(2)}</p>`;
          resultsHtml += '               </div>';
          resultsHtml += `                 <p class="mt-2 text-sm text-gray-500">Precio ${Number(data.Descuento).toFixed(2)}</p>`
          resultsHtml += '             </div>';
          resultsHtml += '  <div class="flex w-28 border border-gray-300 text-gray-600 divide-x divide-gray-300 mt-5">';
          resultsHtml += `  <a  class="h-8 w-8 text-xl flex items-center justify-center cursor-pointer select-none restar" id="restar" data-product-id="${data.item}">-</a>`;
          resultsHtml += `  <div class="h-8 w-10 flex items-center justify-center">${data.quantity}</div>`;
          resultsHtml += `  <a  class="h-8 w-8 text-xl flex items-center justify-center cursor-pointer select-none sumar" id="sumar" data-product-id="${data.item}">+</a>`;
          resultsHtml += '  </div>';
          resultsHtml += '             <div class="flex flex-1 items-end justify-between text-sm mt-5">';
          resultsHtml += `               <p class="text-gray-500">Cantidad ${data.quantity}</p>`;
          resultsHtml += '               <div class="flex">';
          resultsHtml += `<button type="submit" id="ElimianrProducto" class="font-medium text-red-700 hover:text-red-400 ElimianrProducto" data-product-id="${data.item}">Eliminar <i class="fas fa-trash"></i></button>`
          resultsHtml += '               </div>';
          resultsHtml += '             </div>';
          resultsHtml += '           </div>';
          resultsHtml += '         </li>';
          resultsHtml += '         <hr>';

        });
        resultsHtml += '       </ul>';
        resultsHtml += '     </div>';


        var resultsHtml2 = '  <p>Subtotal</p>';
        resultsHtml2 += `   <p>$${dato2.toFixed(2)}</p>`;


        $('#modalintsub').html(resultsHtml2);
        $('#modalint').html(resultsHtml);
      }

    })
    .catch(error => {
      console.error("Error al obtener la cantidad del carrito", error);
    });
  }

  function carritomodal2(){
    fetch(vercarrito)
    .then(response => response.json())
    .then(cartData => {
      

     
      if (cartData['cart_items'] == '' || cartData == ['cart_items'] == undefined) {
        modalcarrito.style.display = (modalcarrito.style.display === 'none') ? 'block' : 'none';
        fetch(cartoCartUrl)
        .then(response => response.json())
        .then(cartData => {
   

          var cartCountElement = document.getElementById("cart-count");
          if (cartCountElement) {
            cartCountElement.textContent = cartData.cart_count;
          }
        })
        .catch(error => {
          console.error("Error al obtener la cantidad del carrito", error);
        });
      } else {
        var datos = cartData['cart_items'];
        var dato2 = Number(cartData['total'])


        var resultsHtml = '     <div class="flow-root">';
        resultsHtml += '       <ul role="list" class="-my-6 divide-y divide-gray-200">';
        datos.forEach(function (data) {
          resultsHtml += '         <li class="flex py-6">';
          resultsHtml += '           <div style="    width: 120px; height: 120px;" class="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">';
          resultsHtml += ` <img src="https://riba.app/imgrs/THUMBS 500X500/${data.item}.jpg" alt="not found class="w-full h-full object-cover object-center" onerror="this.src='https://www.ribasmith.com/media/catalog/product/placeholder/default/watermark_4.png' ">`;
          resultsHtml += '           </div>';
          resultsHtml += '           <div class="ml-5 flex flex-1 flex-col">';
          resultsHtml += '             <div>';
          resultsHtml += '               <div class="flex justify-between text-base font-medium text-gray-900">';
          resultsHtml += '                 <h3>';
          resultsHtml += `                   <a href="#">${data.nombre.slice (0, 12)}...</a>`;
          resultsHtml += '                 </h3>';
          resultsHtml += `                <p class="ml-4 text-indigo-600">$ ${data.total.toFixed(2)}</p>`;
          resultsHtml += '               </div>';
          resultsHtml += `                 <p class="mt-2 text-sm text-gray-500">Precio ${Number(data.Descuento).toFixed(2)}</p>`
          resultsHtml += '             </div>';
          resultsHtml += '  <div class="flex w-28 border border-gray-300 text-gray-600 divide-x divide-gray-300 mt-5">';
          resultsHtml += `  <a  class="h-8 w-8 text-xl flex items-center justify-center cursor-pointer select-none restar" id="restar" data-product-id="${data.item}">-</a>`;
          resultsHtml += `  <div class="h-8 w-10 flex items-center justify-center">${data.quantity}</div>`;
          resultsHtml += `  <a  class="h-8 w-8 text-xl flex items-center justify-center cursor-pointer select-none sumar" id="sumar" data-product-id="${data.item}">+</a>`;
          resultsHtml += '  </div>';
          resultsHtml += '             <div class="flex flex-1 items-end justify-between text-sm mt-5">';
          resultsHtml += `               <p class="text-gray-500">Cantidad ${data.quantity}</p>`;
          resultsHtml += '               <div class="flex">';
          resultsHtml += `<button type="submit" id="ElimianrProducto" class="font-medium text-red-700 hover:text-red-400 ElimianrProducto" data-product-id="${data.item}">Eliminar <i class="fas fa-trash"></i></button>`
          resultsHtml += '               </div>';
          resultsHtml += '             </div>';
          resultsHtml += '           </div>';
          resultsHtml += '         </li>';
          resultsHtml += '         <hr>';
        });
        resultsHtml += '       </ul>';
        resultsHtml += '     </div>';


        var resultsHtml2 = '  <p>Subtotal</p>';
        resultsHtml2 += `   <p>$${dato2.toFixed(2)}</p>`;


        $('#modalintsub').html(resultsHtml2);
        $('#modalint').html(resultsHtml);
        fetch(cartoCartUrl)
        .then(response => response.json())
        .then(cartData => {
          var toast = document.getElementById("toast");
          toast.style.display = "block";
          setTimeout(function () {
            toast.style.display = "none";
          }, 1500);

          var cartCountElement = document.getElementById("cart-count");
          if (cartCountElement) {
            cartCountElement.textContent = cartData.cart_count;
          }
        })
        .catch(error => {
          console.error("Error al obtener la cantidad del carrito", error);
        });
      }
    
    })
    .catch(error => {
      console.error("Error al obtener la cantidad del carrito", error);
    });
  }

  modal()

  function modal() {



    ///carrito de compra sidebar 
    const carritoview = document.getElementById('carritoview');
    const modalcarrito = document.getElementById('modalcarrito');
    const cerrarCarrito = document.getElementById('cerrarCarrito');
    const continuarcomprando = document.getElementById('continuarcomprando');

    continuarcomprando.addEventListener('click', function () {
      // // Alternar la visibilidad del submenú al hacer clic en el botón
      //
      modalcarrito.style.display = (modalcarrito.style.display === 'none') ? 'block' : 'none';
    });

    cerrarCarrito.addEventListener('click', function () {
      // // Alternar la visibilidad del submenú al hacer clic en el botón
      //
      modalcarrito.style.display = (modalcarrito.style.display === 'none') ? 'block' : 'none';
    });

    // Agregar un controlador de eventos al botón "Company"
    carritoview.addEventListener('click', function () {
      // // Alternar la visibilidad del submenú al hacer clic en el botón
      //
      carritomodal()


    });
  }



  $(document).on("click", ".ElimianrProducto", function () {
    Swal.fire({
      title: '¿Estás seguro?',
      text: "¡No podrás revertir esto!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      cancelButtonText: 'No',
      confirmButtonText: 'Si, Eliminar'
    }).then((result) => {
    
      if (result.isConfirmed) {

      
        var product_id = $(this).data("product-id");
        var urlfinal = urlfinaldelete.replace('0', product_id)
        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    
        $.ajax({
          url: urlfinal,
          method: "POST",
          dataType: "json",
          headers: {
            "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
          },
          success: function (data) {
    
            if (data.status === "success") {
    
              carritomodal2()
            }
          }
        })
      }
 

  
  })
  })
    $(document).on("click", ".sumar", function () {

    var product_id = $(this).data("product-id");
    var urlfinal = addToCartUrl.replace('0', product_id)
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      url: urlfinal,
      method: "POST",
      dataType: "json",
      headers: {
        "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
      },
      success: function (data) {

        if (data.status === "success") {

          carritomodal2()
        }
      }
    })
  })

  $(document).on("click", ".restar", function () {

    var product_id = $(this).data("product-id");
    var urlfinal = urlremove_cart.replace('0', product_id)
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      url: urlfinal,
      method: "POST",
      dataType: "json",
      headers: {
        "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
      },
      success: function (data) {

        if (data.status === "success") {

          carritomodal2()
        }
      }
    })
  })
  $(document).on("click", ".EliminarCarrito", function () {

    Swal.fire({
      title: '¿Estás seguro?',
      text: "¡No podrás revertir esto!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      cancelButtonText: 'No',
      confirmButtonText: 'Si, Eliminar'
    }).then((result) => {
      
      if (result.isConfirmed) {

        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    
        $.ajax({
          url: urlrEliminarCarrtioCompleto,
          method: "POST",
          dataType: "json",
          headers: {
            "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
          },
          success: function (data) {
    
            if (data.status === "success") {
    
              carritomodal2()
            }
          }
        })
      }
    })
    // Swal.fire({
    //   title: 'Do you want to save the changes?',
    //   showDenyButton: true,
    //   showCancelButton: true,
    //   confirmButtonText: 'Save',
    //   denyButtonText: `Don't save`,
    // }).then((result) => {
    //   /* Read more about isConfirmed, isDenied below */
    //   if (result.isConfirmed) {
    //     Swal.fire('Saved!', '', 'success')
    //   } else if (result.isDenied) {
    //     Swal.fire('Changes are not saved', '', 'info')
    //   }
    // })
  
  })





  ////pertenece al checkoout 


  const tarjetaFormulario = document.getElementById("tarjetaFormulario");
  const type1RadioButton = document.getElementById("type1");
  const type2RadioButton = document.getElementById("type2");
  const type3RadioButton = document.getElementById("type3");
  // Escucha cambios en la selección del radio button
  type3RadioButton.addEventListener("change", function () {
      if (type3RadioButton.checked) {
          tarjetaFormulario.style.display = "none"; // Oculta el formulario de tarjeta
      }
  });
  type2RadioButton.addEventListener("change", function () {
      if (type2RadioButton.checked) {
          tarjetaFormulario.style.display = "none"; // Oculta el formulario de tarjeta
      }
  });
  
  type1RadioButton.addEventListener("change", function () {
      if (type1RadioButton.checked) {
          tarjetaFormulario.style.display = "block"; // Muestra el formulario de tarjeta
      }
  });



///inicia el mapa del checkout
  function initMap() {
    if ("geolocation" in navigator) {
      // El navegador soporta geolocalización
      navigator.geolocation.getCurrentPosition(function(position) {
        // Se ha obtenido la ubicación del usuario
        var latitud = position.coords.latitude;
        var longitud = position.coords.longitude;
  
        // Crea un objeto de mapa de Google Maps y lo muestra en el elemento con el ID "map"
        var map = new google.maps.Map(document.getElementById('map'), {
          center: { lat: latitud, lng: longitud },
          zoom: 15 // Nivel de zoom
        });
  
        // Crea un marcador inicial en la ubicación del usuario
        var marker = new google.maps.Marker({
          position: { lat: latitud, lng: longitud },
          map: map,
          draggable: true // Permite que el marcador sea movible
        });
  
        // Agrega un evento para escuchar cuando se arrastra el marcador
        marker.addListener('dragend', function(event) {
          var newLatitud = event.latLng.lat();
          var newLongitud = event.latLng.lng();
          
          // Actualiza la posición del marcador en la página
          document.getElementById('coordenadas').textContent = "Latitud: " + newLatitud + ", Longitud: " + newLongitud;
        });
  
        // También puedes mostrar las coordenadas en la página
        document.getElementById('coordenadas').textContent = "Latitud: " + latitud + ", Longitud: " + longitud;
      }, function(error) {
        // Manejar errores de geolocalización
        switch (error.code) {
          case error.PERMISSION_DENIED:
            console.error("El usuario ha denegado la solicitud de geolocalización.");
            break;
          case error.POSITION_UNAVAILABLE:
            console.error("La información de ubicación no está disponible.");
            break;
          case error.TIMEOUT:
            console.error("Se ha agotado el tiempo de espera para obtener la ubicación.");
            break;
          case error.UNKNOWN_ERROR:
            console.error("Se ha producido un error desconocido.");
            break;
        }
      });
    } else {
      // El navegador no soporta geolocalización
      console.error("La geolocalización no es compatible en este navegador.");
    }
  }
  
  
    initMap();


    $(document).ready(function () {

      setTimeout(function () {
          $('#messages').fadeOut('slow')
      }, 4000)
  });
  

  const datapicker  = document.getElementById('test');

  new Datepicker(datapicker, {
      todayHighlight: true,
      minDate: new Date()
  });
})



///funcion de store

///sidebar de filtrado
document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.querySelector(".sidebar");
  const toggleFilterButton = document.querySelector(".toggle-filter-button");



  // Agrega un evento clic al botón de filtro
  toggleFilterButton.addEventListener("click", function () {
      // Toggle (mostrar/ocultar) el sidebar al hacer clic en el botón
      sidebar.classList.toggle("hidden");
  });

  $("#cerrar").click(function () {
  sidebar.classList.toggle("hidden");
});



//funcion de product_detail 

//contador
let numero = 0;
masbtn.onclick = () => {
    numero++;
    cantidad.value = numero;
}

rest.onclick = () => {

    if (numero < 1) {

    } else {
        numero--;
        cantidad.value = numero;
    }


}



});
