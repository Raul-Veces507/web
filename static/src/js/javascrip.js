$(document).ready(function () {




  $(".add-to-cart-button").click(function () {


    var itemproducts = $(this).data("product-id")

    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    var postData = {
      item: itemproducts,
    };
    $.ajax({
      url: ValidarCarrito,
      method: "POST",
      dataType: "json",
      headers: {
        "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
      },
      data: postData, // Envía los datos como objeto JSON
      success: function (data) {

        if (data.status === "success") {
          modaldetalle(itemproducts)

        }  else if (data.status === "warning"){
          Agregarlocal(itemproducts)
        }else{
          alert(data);
        }
      }
    })

  })

  function Agregarlocal(data){


    var product_id = data
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
  }


function modaldetalle (data){
  const addproduct = document.getElementById("addproduct");
  const overlayElement = document.getElementById("overlay");

  addproduct.classList.remove("hidden");
  overlayElement.classList.remove("hidden");


  var product_id = data
  const Addproductomodal = document.getElementById("Addproductomodal");

  var resultsHtml ='<h3 class="mb-4 font-semibold text-gray-900 dark:text-white">Comentario</h3>'
  resultsHtml += '<ul class="items-center w-full text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg sm:flex dark:bg-gray-700 dark:border-gray-600 dark:text-white">'
  resultsHtml += '    <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">'
  resultsHtml += '        <div class="flex items-center pl-3">'
  resultsHtml += '            <input id="ComentarioSi" type="radio" value="" name="list-radio2"'
  resultsHtml += '                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">'
  resultsHtml += '            <label for="ComentarioSi"'
  resultsHtml += '                class="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Si'
  resultsHtml += '            </label>'
  resultsHtml += '        </div>'
  resultsHtml += '    </li>'
  resultsHtml += '    <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">'
  resultsHtml += '        <div class="flex items-center pl-3">'
  resultsHtml += '            <input id="ComentarioNo" type="radio" value="" name="list-radio2" checked'
  resultsHtml += '                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">'
  resultsHtml += '            <label for="ComentarioNo"'
  resultsHtml += '                class="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">No</label>'
  resultsHtml += '        </div>'
  resultsHtml += '    </li>'
 
  
  resultsHtml += '</ul>'
  resultsHtml += '<div class="mt-5 hidden" id="ComentarioText">'
  resultsHtml += '    <label for="message" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Comentario</label>'
  resultsHtml += `    <input type="hidden" name="itemproducts" id="itemproducts" value="${product_id}">`

  resultsHtml += '    <textarea id="message" rows="4" name="message" maxlength="130" '
  resultsHtml += '        class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"'
  resultsHtml += '        placeholder="Ingrese un Comentario para el producto..."></textarea>'
  resultsHtml += '</div>'
  resultsHtml += '<h3 class="mb-4 font-semibold text-gray-900 dark:text-white mt-5">Remplazar Producto</h3>'
  resultsHtml += '<p class="text-sm font-normal text-gray-500 dark:text-gray-400">Desea Remplazar El Producto Si No Se Encuentra?</p>'
  resultsHtml += '<ul  class="items-center w-full text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg sm:flex dark:bg-gray-700 dark:border-gray-600 dark:text-white mt-5">'
  resultsHtml += '    <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">'
  resultsHtml += '        <div class="flex items-center pl-3">'
  resultsHtml += '            <input id="BuscadorSi" type="radio" value="" name="list-radio1"'
  resultsHtml += '                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">'
  resultsHtml += '            <label for="BuscadorSi"'
  resultsHtml += '                class="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Si'
  resultsHtml += '            </label>'
  resultsHtml += '        </div>'
  resultsHtml += '    </li>'
  resultsHtml += '    <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">'
  resultsHtml += '        <div class="flex items-center pl-3">'
  resultsHtml += '            <input id="BuscadorNo" type="radio" value="" name="list-radio1" checked'
  resultsHtml += '                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">'
  resultsHtml += '            <label for="BuscadorNo"'
  resultsHtml += '                class="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">No</label>'
  resultsHtml += '        </div>'
  resultsHtml += '    </li>'

  resultsHtml += '</ul>'
  
  resultsHtml += '<div class="mt-5 hidden rounded-xl" id="BuscadorInputs"">'
  resultsHtml += '    <label for="message" class="block mb-2 text-sm font-bold text-gray-900 dark:text-white">Buscar Producto Remplazo</label>'
  resultsHtml += '<input type="text" id="search-input-modal" class="pl-13 w-full py-3 px-3 mt-5 rounded-xl" placeholder="busqueda" autocomplete="off">'
  resultsHtml += '<div class="  w-full mt-4  mb-2" >'
 
  resultsHtml+='<h3 class="mb-4 font-semibold text-gray-900 dark:text-white">Filtros</h3>'
  resultsHtml+='<ul class=" flex items-center w-full text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg sm:flex dark:bg-gray-700 dark:border-gray-600 dark:text-white">'
  resultsHtml+=' <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">'
  resultsHtml+=' <div class="flex items-center pl-3">'
  resultsHtml+=' <input id="vue-checkbox-list" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">'
  resultsHtml+=' <label for="vue-checkbox-list" class="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Vue JS</label>'
  resultsHtml+='</div>'
  resultsHtml+=' </li>'
  resultsHtml+=' <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">'
  resultsHtml+=' <div class="flex items-center pl-3">'
  resultsHtml+=' <input id="vue-checkbox-list" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">'
  resultsHtml+=' <label for="vue-checkbox-list" class="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Vue JS</label>'
  resultsHtml+='</div>'
  resultsHtml+=' </li>'
  resultsHtml+=' <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">'
  resultsHtml+=' <div class="flex items-center pl-3">'
  resultsHtml+=' <input id="vue-checkbox-list" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">'
  resultsHtml+=' <label for="vue-checkbox-list" class="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Vue JS</label>'
  resultsHtml+='</div>'
  resultsHtml+=' </li>'
  
  
  
  
  resultsHtml+='</ul>'


  


  resultsHtml += '</div>'
  resultsHtml += '</div>'
  resultsHtml += '<div id="search-results-modal"'
  resultsHtml += 'class="">'
  
  resultsHtml += '</div>'

 
 resultsHtml+='</div>'


  Addproductomodal.innerHTML = resultsHtml; // Asume que `resultsHtml` contiene el contenido HTML
  function handleRadioChange(radio, targetId, show) {
    const target = document.getElementById(targetId);
    if (radio.checked) {
      if (show) {
        target.classList.remove("hidden");
      } else {
        target.classList.add("hidden");
      }
    }
  }

  const type1 = document.getElementById("ComentarioSi");
  const type2 = document.getElementById("ComentarioNo");
  const type3 = document.getElementById("BuscadorSi");
  const type4 = document.getElementById("BuscadorNo");

  type1.addEventListener("change", () => {
    handleRadioChange(type1, "ComentarioText", true);
    
  });

  type2.addEventListener("change", () => {
    handleRadioChange(type2, "ComentarioText", false);
    const textarea = document.getElementById("message");
    textarea.value = ""; // Esto vaciará el contenido del textarea
  });

  type3.addEventListener("change", () => {
    handleRadioChange(type3, "BuscadorInputs", true);
  });

  type4.addEventListener("change", () => {
    handleRadioChange(type4, "BuscadorInputs", false);
  });







}




  $(".agregarCarritoProduct").click(function () {
    
    var itemproducts = $("#itemproducts").val();
    var productMessage = $("#message").val();
    var NewselectedProduct = $("input[name='productBuscador']:checked").val();

    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    var postData = {
      item: itemproducts,
      Comentario: productMessage,
      Newproduct: NewselectedProduct
    };
    $.ajax({
      url: agregarCarritoUrl,
      method: "POST",
      dataType: "json",
      headers: {
        "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
      },
      data: postData, // Envía los datos como objeto JSON
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
              const addproduct = document.getElementById("addproduct");
              const overlayElement = document.getElementById("overlay");
          
              addproduct.classList.add("hidden");
              overlayElement.classList.add("hidden");
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
          const addproduct = document.getElementById("addproduct");
          const overlayElement = document.getElementById("overlay");
      
          addproduct.classList.add("hidden");
          overlayElement.classList.add("hidden");
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



  $(".cerrarModalStore").click(function () {

    const addproduct = document.getElementById("addproduct");
    const overlayElement = document.getElementById("overlay");

    addproduct.classList.add("hidden");
    overlayElement.classList.add("hidden");

  })

  $(".cerrarModalStore2").click(function () {


    const addproduct = document.getElementById("addproduct");
    const overlayElement = document.getElementById("overlay");

    addproduct.classList.add("hidden");
    overlayElement.classList.add("hidden");

  })

  function BuscadorModal(inputElement, resultElement) {
    let typingTimer;
    const delay = 1000; // Tiempo en milisegundos para esperar después de dejar de escribir

    $(document).on('input', inputElement, function () {
      var query = $(this).val();

      // Borra el temporizador anterior si existe
      clearTimeout(typingTimer);

      // Inicia un nuevo temporizador
      typingTimer = setTimeout(function () {
        const bodega = storedValue
        console.log(storedValue);
        if (query.length >= 2) { // Evitar búsquedas vacías o muy cortas
        
          var requestData = { "busqueda": query,"bodega":bodega };
          $.ajax({
            url: 'http://192.168.88.136:3005/ecommer/rs/buscador',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(requestData),

            success: function (data) {
              console.log(data);
              // Procesa los datos de la API y muestra los resultados

              var datos = data['productos'];

              var resultsHtml = '<div class="grid grid-cols-1 sm:grid-cols-4 gap-4">';

              datos.slice(0, 4).forEach(function (product) {


                resultsHtml += '<ul class="p-3 space-y-1 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownHelperRadioButton">'
                resultsHtml += '<li>'
                resultsHtml += '  <div class="flex p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600">'
                resultsHtml += '    <div class="flex items-center h-5">'
                resultsHtml += `        <input id="${product.item}" value="${product.item}" name="productBuscador" type="radio" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">`
                resultsHtml += '    </div>'
                resultsHtml += '    <div class="flex-shrink-0 ml-5">'
                resultsHtml += `      <img class="w-8 h-8 rounded-full" src="https://riba.app/imgrs/THUMBS 500X500/${product.item}.jpg" alt="{{product.nombre}}" onerror="this.src='https://www.ribasmith.com/media/catalog/product/placeholder/default/watermark_4.png'">`
                resultsHtml += '    </div>'
                resultsHtml += '    <div class="ml-2 text-sm">'
                resultsHtml += `        <label for="${product.item}" class="font-medium text-gray-900 dark:text-gray-300">`
                resultsHtml += `          <div>${product.nombre}</div>`
                resultsHtml += `          <p id="helper-radio-text-4" class="text-xs font-normal text-gray-500 dark:text-gray-300">$ ${product.precio}</p>`
                resultsHtml += '        </label>'
                resultsHtml += '    </div>'
                resultsHtml += '  </div>'
                resultsHtml += '  </li>'
                resultsHtml += ' </ul>'
              });


              resultsHtml += '</div>';
              // Cierra el contenedor con barra de desplazamiento
              $(resultElement).html(resultsHtml);
            },
            error: function () {
              // Maneja errores de la solicitud AJAX
              $(resultElement).html('Error en la búsqueda.');
            }
          });
        } else {
          $(resultElement).html('');
        }
      }, delay); // Establece el retraso antes de realizar la búsqueda
    });
  }

  // Llama a la función para los campos de búsqueda dentro del modal
  BuscadorModal('#search-input-modal', '#search-results-modal');



  ////eliminar Productos del carrito


  function carritomodal() {
    fetch(vercarrito)
      .then(response => response.json())
      .then(cartData => {

        if (cartData['cart_items'] == '' || cartData['cart_items'] == undefined) {
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
            resultsHtml += `                   <a href="#">${data.nombre.slice(0, 12)}...</a>`;
            resultsHtml += '                 </h3>';
            resultsHtml += `                <p class="ml-4 text-indigo-600">$ ${Number(data.precio)*Number(data.quantity)}</p>`;
            resultsHtml += '               </div>';
            
              resultsHtml += `                 <p class="mt-2 text-sm text-gray-500">Precio ${Number(data.precio).toFixed(2)}</p>`
        
           
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

  function carritomodal2() {
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
            resultsHtml += `                   <a href="#">${data.nombre.slice(0, 12)}...</a>`;
            resultsHtml += '                 </h3>';
            resultsHtml += `                <p class="ml-4 text-indigo-600">$ ${Number(data.precio)*Number(data.quantity)}</p>`;
            resultsHtml += '               </div>';
              resultsHtml += `                 <p class="mt-2 text-sm text-gray-500">Precio ${Number(data.precio).toFixed(2)}</p>`
           
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
      navigator.geolocation.getCurrentPosition(function (position) {
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
        marker.addListener('dragend', function (event) {
          var newLatitud = event.latLng.lat();
          var newLongitud = event.latLng.lng();

          // Actualiza la posición del marcador en la página
          document.getElementById('coordenadas').textContent = "Latitud: " + newLatitud + ", Longitud: " + newLongitud;
        });

        // También puedes mostrar las coordenadas en la página
        document.getElementById('coordenadas').textContent = "Latitud: " + latitud + ", Longitud: " + longitud;
      }, function (error) {
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




  const datapicker = document.getElementById('test');

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







});
