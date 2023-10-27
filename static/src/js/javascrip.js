$(document).ready(function () {




  $(".add-to-cart-button").click(function () {


    var itemproducts = $(this).data("product-id")
    var inventario = $(this).data("product-id2")
    var inventioProducto=$(this).data("product-inv")
    var cantidadAgregada=$(this).data("product-cant")

    if(cantidadAgregada== undefined  || inventioProducto==undefined){
        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
        console.log(csrfToken);
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
    
            if (data.status == "success") {
              if(inventario<=10){
                modaldetalle(itemproducts)
                obtener(itemproducts)
              }else{
                  Agregarlocal(itemproducts)
             
  
              }
    
    
            } else if (data.status == "warning") {
       
              if(Number(data.data)>=Number(inventario)){
                var elemento = document.getElementById("toasterror");
        
                // Asigna un nuevo texto al elemento
                elemento.textContent = "Limite de producto Alcanzado";
                elemento.style.display = "block";
                setTimeout(function () {
                elemento.style.display = "none";
                }, 1500);
              }else{
                Agregarlocal(itemproducts)
            
              }
            } else {
              var elemento = document.getElementById("toasterror");
            
              // Asigna un nuevo texto al elemento
              elemento.textContent = "Error No Se pudo Agregar Al Carrito";
              elemento.style.display = "block";
              setTimeout(function () {
              elemento.style.display = "none";
              }, 1500);
             
            }
          }
        })
        
    }else{
      if(cantidadAgregada>=inventioProducto){

        var elemento = document.getElementById("toasterror");
  
        // Asigna un nuevo texto al elemento
        elemento.textContent = "Limite de producto Alcanzado";
        elemento.style.display = "block";
        setTimeout(function () {
        elemento.style.display = "none";
        }, 1500);
      }else{
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
            if(inventario<=10){
              modaldetalle(itemproducts)
              obtener(itemproducts)
            }else{
              Agregarlocal(itemproducts)
            }
  
  
          } else if (data.status == "warning") {
             if(Number(data.data)>=Number(inventario)){
               var elemento = document.getElementById("toasterror");
             
               // Asigna un nuevo texto al elemento
               elemento.textContent = "Limite de producto Alcanzado";
               elemento.style.display = "block";
               setTimeout(function () {
               elemento.style.display = "none";
               }, 1500);
             }else{
               Agregarlocal(itemproducts)
           
             }
           } else {
             var elemento = document.getElementById("toasterror");
             
             // Asigna un nuevo texto al elemento
             elemento.textContent = "Error No Se pudo Agregar Al Carrito";
             elemento.style.display = "block";
             setTimeout(function () {
             elemento.style.display = "none";
             }, 1500);
            
           }
        }
      })
      }
    }
  
  




  })

  function Agregarlocal(data) {


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


  function modaldetalle(data) {

    const addproduct = document.getElementById("addproduct");
    const overlayElement = document.getElementById("overlay");

    addproduct.classList.remove("hidden");
    overlayElement.classList.remove("hidden");


    var product_id = data
    const Addproductomodal = document.getElementById("Addproductomodal");

    var resultsHtml = '<h3 class="mb-4 font-semibold text-gray-900 dark:text-white mt-5">Remplazar Producto</h3>'
    resultsHtml += '<p class="text-sm font-normal text-gray-500 dark:text-gray-400">Desea Remplazar El Producto Si No Se Encuentra?</p>'

    resultsHtml += `<input type="hidden" value="${product_id}" name="itemproducts" id="itemproducts">`
    resultsHtml += '<div class="flex mt-5">'
    resultsHtml += '  <ul class="grid w-full gap-6 md:grid-cols-2">'
    resultsHtml += '  <li>'
    resultsHtml += '      <input type="radio" id="BuscadorSi" name="hosting"  class="hidden peer" required>'
    resultsHtml += '      <label for="BuscadorSi" class="inline-flex items-center justify-between w-full p-5 text-gray-500 bg-white border border-gray-200 rounded-lg cursor-pointer dark:hover:text-gray-300 dark:border-gray-700 dark:peer-checked:text-blue-500 peer-checked:border-blue-600 peer-checked:text-blue-600 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700 radio-label-hover">                           '
    resultsHtml += '          <div class="block">'
    resultsHtml += '              <div class="w-full text-lg font-semibold">Si</div>'
    resultsHtml += '              <div class="w-full">Deseo Remplazar El Producto </div>'
    resultsHtml += '          </div>'
    resultsHtml += '      </label>'
    resultsHtml += '  </li>'
    resultsHtml += '  <li>'
    resultsHtml += '      <input type="radio" id="BuscadorNo" name="hosting"  class="hidden peer" checked>'
    resultsHtml += '      <label for="BuscadorNo" class="inline-flex items-center justify-between w-full p-5 text-gray-500 bg-white border border-gray-200 rounded-lg cursor-pointer dark:hover:text-gray-300 dark:border-gray-700 dark:peer-checked:text-blue-500 peer-checked:border-blue-600 peer-checked:text-blue-600 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700 radio-label-hover">'
    resultsHtml += '          <div class="block">'
    resultsHtml += '              <div class="w-full text-lg font-semibold">No</div>'
    resultsHtml += '              <div class="w-full">No Deseo Remplazar El Producto</div>'
    resultsHtml += '          </div>'
    resultsHtml += '      </label>'
    resultsHtml += '  </li>'
    
    resultsHtml += '</ul>'
    resultsHtml += '  </div>'

    

    resultsHtml += '<div class="mt-5 hidden rounded-xl" id="BuscadorInputs"">'
    resultsHtml += '<div class="relative overflow-x-auto shadow-md sm:rounded-lg">'
    resultsHtml += '    <div class="flex items-center justify-between pb-4 bg-white dark:bg-gray-900">'
    resultsHtml += '        <label for="table-search" class="sr-only">Search</label>'
    resultsHtml += '        <div class="relative">'
    resultsHtml += '            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">'
    resultsHtml += '                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">'
    resultsHtml += '                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>'
    resultsHtml += '                </svg>'
    resultsHtml += '            </div>'
    resultsHtml += '            <input type="text" id="table-search-users" class=" w-full block p-2 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg  bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Buscar Producto">'
    resultsHtml += '        </div>'
    resultsHtml += '    </div>'
    resultsHtml += '<div  id="Marcaschecbock">'
    resultsHtml += ' </div>'

    resultsHtml += '<div class="container grid lg:grid-cols-4 gap-6 pt-4 pb-16 items-start relative " id="productos">'
    resultsHtml += ' </div>'

    resultsHtml += '<div class="mt-5" id="botonoesnav">'
    resultsHtml += '<nav class="flex items-center justify-between pt-4 mb-4 mx-4" aria-label="Table navigation">'
    resultsHtml += '    <span class="text-sm font-normal text-gray-500 dark:text-gray-400" id="resultados-span"></span>'
    resultsHtml += '    <ul class="inline-flex -space-x-px text-sm h-8">'
    resultsHtml += '        <li>'
    resultsHtml += '            <button id="previous-page" class="flex items-center justify-center px-3 h-8 ml-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-l-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Anterior</button>'
    resultsHtml += '        </li>'

    resultsHtml += '        <li>'
    resultsHtml += '            <button id="next-page" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-r-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Siguiente</button>'
    resultsHtml += '        </li>'
    resultsHtml += '     </ul>'
    resultsHtml += ' </nav>'
    resultsHtml += '</div>'

    resultsHtml += '</div>'




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

    const type3 = document.getElementById("BuscadorSi");
    const type4 = document.getElementById("BuscadorNo");


    type3.addEventListener("change", () => {
      handleRadioChange(type3, "BuscadorInputs", true);
    });

    type4.addEventListener("change", () => {
      handleRadioChange(type4, "BuscadorInputs", false);
    });







  }

  function obtener(data) {


    const productosslide = document.getElementById("productos");
    const Marcaschecbock = document.getElementById("Marcaschecbock");

    var itemproducts = data

    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    var postData = {
      item: itemproducts,
    };
    $.ajax({
      url: obtenerinfoproduct,
      method: "POST",
      dataType: "json",
      headers: {
        "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
      },
      data: postData, // Envía los datos como objeto JSON
      success: function (data) {

        const productos = data['productos'].productos
        const Marcas = data['productos'].MarcaUnicas

        // const productos = data['productos'].productos;
        const resultadosPorPagina = 12; // Número de resultados por página
        let paginaActual = 1; // Página actual

        // Dividir la lista de productos en páginas
        const paginas = [];
        for (let i = 0; i < productos.length; i += resultadosPorPagina) {
          paginas.push(productos.slice(i, i + resultadosPorPagina));
        }
        mostrarResultados()

        function mostrarResultados() {

          const resultadosMostrados = (paginaActual - 1) * resultadosPorPagina + 1;
          const resultadosFinales = Math.min(paginaActual * resultadosPorPagina, productos.length);
          const totalResultados = productos.length;

          const resultadosSpan = document.getElementById('resultados-span'); // Reemplaza 'resultados-span' con el ID o clase correcta
          resultadosSpan.textContent = `Showing ${resultadosMostrados}-${resultadosFinales} of ${totalResultados}`;

          const productosPagina = paginas[paginaActual - 1];
          // Recorre los datos y agrégalos a la tabla


          var resp2 = '<div class="scroll-container space-x-2 mb-4 mt-5" style=" height: 60px;   width: 100%; overflow-x: auto; white-space: nowrap; display: inline-block;">';
          resp2 += `<input id="Todos" checked type="radio" value="Todos" name="radiocheck" class=" radiocheck w-4 h-4 text-red-600 bg-gray-100 border-gray-300 focus:ring-red-500 dark:focus:ring-red-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">`;
          resp2 += `<label for="Todos" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Todos</label>`;
          Marcas.forEach((Marca) => {
 
            resp2 += '<div class="item" style="display: inline-block;">';
            resp2 += `<input id="${Marca.name}" type="radio" value="${Marca.name}" name="radiocheck" class=" radiocheck w-4 h-4 text-red-600 bg-gray-100 border-gray-300 focus:ring-red-500 dark:focus:ring-red-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">`;
            resp2 += `<label for="${Marca.name}" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">${Marca.name}</label>`;
            resp2 += '</div>';
          });

          resp2 += '</div>';
          Marcaschecbock.innerHTML = resp2;


          var resp = '<div >'

          productosPagina.forEach((producto) => {

            resp += ' <div class="w-auto md:w-56 h-auto group rounded bg-white shadow overflow-hidden">'
            resp += `<input type="radio" id="${producto.item}" value="${producto.item}" name="productBuscador" class="hidden peer" required>`
            resp += ` <label for="${producto.item}" class="flex flex-col flex-wrap content-stretch w-full p-5 text-gray-500 bg-white border border-gray-200 rounded-lg cursor-pointer dark:hover:text-gray-300 dark:border-gray-700 dark:peer-checked:text-blue-500 peer-checked:border-blue-600 peer-checked:text-blue-600 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700"> `
            resp += `          <img src=" https://riba.app/imgrs/THUMBS 500X500/${producto.item}.jpg " class=" justify-center mx-auto w-16 h-16 rounded-full>"`
            resp += '     <div class="pt-4 pb-3 px-4 ">'
            resp += `        <h4 class="mt-4 justify-center font-medium  mb-2 text-gray-800 transition  text-limit">  ${producto.nombre}        </h4>`
            resp += '         <div class="flex items-baseline mb-1 space-x-2 justify-center  content-center">'
            if (producto.flagoferta == 1) {
              resp += `       <p class="text-sm text-red-700  font-roboto line-through">$ ${producto.precioRegular}</p>`
              resp += `             <p class="text-xl  text-gray-900 font-roboto font-semibold">$ ${producto.precio}</p>`
            } else {

              resp += `             <p class="text-xl  text-gray-900 font-roboto font-semibold">$ ${producto.precio}`
              resp += '             </p>'
            }

            resp += '           </div>'
            resp += '       </div>'
             resp += '</label>'


            resp += '       </div>'
          });
          resp += '      </div>'

          productosslide.innerHTML = resp;


          ///filtrar por marca 
          // Agrega un evento de escucha a los elementos de radio
          const elementosRadioConjunto1 = document.querySelectorAll('input[name="radiocheck"]');
          elementosRadioConjunto1.forEach((radio) => {
            radio.addEventListener("change", function () {
              const elementoSeleccionado = this.value;
              

              const divdisable = document.getElementById("botonoesnav");
             
          
              if(elementoSeleccionado=='Todos'){
                divdisable.style.display = "block";
                paginaActual = 1;
                mostrarResultados();
              }else{
                divdisable.style.display = "none";
                filtrarElementos(elementoSeleccionado);
              }
         
              // filtrarElementosConjunto1(elementoSeleccionado);
            });
          });
          function filtrarElementos(terminoBusqueda) {
            // Filtra los elementos basados en el término de búsqueda
            const elementosFiltrados = productos.filter((Marca) =>
              Marca.Marca.toLowerCase().includes(terminoBusqueda.toLowerCase())
            );
            
          
            // Muestra los elementos filtrados en el registro
          
            mostrarElementos(elementosFiltrados);
          }

          function mostrarElementos(elementos) {
            var resp = '<div >'

            elementos.forEach((producto) => {

              resp += ' <div class="w-auto md:w-56 h-auto group rounded bg-white shadow overflow-hidden">'
              resp += `<input type="radio" id="${producto.item}" value="${producto.item}" name="productBuscador" class="hidden peer" required>`
              resp += ` <label for="${producto.item}" class="flex flex-col flex-wrap content-stretch w-full p-5 text-gray-500 bg-white border border-gray-200 rounded-lg cursor-pointer dark:hover:text-gray-300 dark:border-gray-700 dark:peer-checked:text-blue-500 peer-checked:border-blue-600 peer-checked:text-blue-600 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700"> `
              resp += `          <img src=" https://riba.app/imgrs/THUMBS 500X500/${producto.item}.jpg " class=" justify-center mx-auto w-16 h-16 rounded-full>"`
              resp += '     <div class="pt-4 pb-3 px-4 ">'
              resp += `        <h4 class="mt-4 justify-center font-medium  mb-2 text-gray-800 transition  text-limit">  ${producto.nombre}        </h4>`
              resp += '         <div class="flex items-baseline mb-1 space-x-2 justify-center  content-center">'
              if (producto.flagoferta == 1) {
                resp += `       <p class="text-sm text-red-700  font-roboto line-through">$ ${producto.precioRegular}</p>`
                resp += `             <p class="text-xl  text-gray-900 font-roboto font-semibold">$ ${producto.precio}</p>`
              } else {
  
                resp += `             <p class="text-xl  text-gray-900 font-roboto font-semibold">$ ${producto.precio}`
                resp += '             </p>'
              }
  
              resp += '           </div>'
              resp += '       </div>'
               resp += '</label>'
  
  
              resp += '       </div>'
            });
            resp += '      </div>'

          productosslide.innerHTML = resp;
          }
          
          

          ///buscador 

          const campoBusqueda = document.getElementById("table-search-users");
          campoBusqueda.addEventListener("input", function () {
            const filtro = campoBusqueda.value.toLowerCase();
            if (filtro === "") {
              // El campo de búsqueda está vacío, restablece la página a 1 y muestra resultados
              paginaActual = 1;
              mostrarResultados();
            } else {
              // Filtra los productos según el criterio de búsqueda
              const productosFiltrados = productos.filter((producto) => {
                const productoNombre = producto.nombre.toLowerCase();
                return productoNombre.includes(filtro);
              });

              var resp = '  <div class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 sm:grid-cols-3 gap-6">'

              productosFiltrados.forEach((producto) => {

                resp += ' <div class="w-auto md:w-56 h-auto group rounded bg-white shadow overflow-hidden">'
                resp += `<input type="radio" id="${producto.item}" value="${producto.item}" name="productBuscador" class="hidden peer" required>`
                resp += ` <label for="${producto.item}" class="flex flex-col flex-wrap content-stretch w-full p-5 text-gray-500 bg-white border border-gray-200 rounded-lg cursor-pointer dark:hover:text-gray-300 dark:border-gray-700 dark:peer-checked:text-blue-500 peer-checked:border-blue-600 peer-checked:text-blue-600 hover:text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700"> `
                resp += `          <img src=" https://riba.app/imgrs/THUMBS 500X500/${producto.item}.jpg " class=" justify-center mx-auto w-16 h-16 rounded-full>"`
                resp += '     <div class="pt-4 pb-3 px-4 ">'
                resp += `        <h4 class="mt-4 justify-center font-medium  mb-2 text-gray-800 transition  text-limit">  ${producto.nombre}        </h4>`
                resp += '         <div class="flex items-baseline mb-1 space-x-2 justify-center  content-center">'
                if (producto.flagoferta == 1) {
                  resp += `       <p class="text-sm text-red-700  font-roboto line-through">$ ${producto.precioRegular}</p>`
                  resp += `             <p class="text-xl  text-gray-900 font-roboto font-semibold">$ ${producto.precio}</p>`
                } else {
    
                  resp += `             <p class="text-xl  text-gray-900 font-roboto font-semibold">$ ${producto.precio}`
                  resp += '             </p>'
                }
    
                resp += '           </div>'
                resp += '       </div>'
                 resp += '</label>'
    
    
                resp += '       </div>'
              });
              resp += '      </div>'

              productosslide.innerHTML = resp;





            }



          });

        }



        const previousPageButton = document.getElementById('previous-page');
        const nextPageButton = document.getElementById('next-page');

        previousPageButton.addEventListener('click', () => {
          if (paginaActual > 1) {
            paginaActual--;
            mostrarResultados();

          }
        });

        nextPageButton.addEventListener('click', () => {
          if (paginaActual < paginas.length) {
            paginaActual++;
            mostrarResultados();
          }
        });





      }
    })



    // Accede a la tabla por su ID







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


  //eliminar Productos del carrito


  function carritomodal() {
    fetch(vercarrito)
      .then(response => response.json())
      .then(cartData => {

        if (cartData['cart_items'] == '' || cartData['cart_items'] == undefined) {
          window.location.href = carrito;
        } else {
          modalcarrito.style.display = (modalcarrito.style.display === 'none') ? 'block' : 'none';
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
            resultsHtml += `                <p class="ml-4 text-indigo-600">$ ${(Number(data.precio) * Number(data.quantity)).toFixed(2)}</p>`;
            resultsHtml += '               </div>';

            resultsHtml += `                 <p class="mt-2 text-sm text-gray-500">Precio ${Number(data.precio).toFixed(2)}</p>`


            resultsHtml += '             </div>';
            resultsHtml += '  <div class="flex w-28 border border-gray-300 text-gray-600 divide-x divide-gray-300 mt-5">';
            resultsHtml += `  <a  class="h-8 w-8 text-xl flex items-center justify-center cursor-pointer select-none restar" id="restar" data-product-id="${data.item}">-</a>`;
            resultsHtml += `  <div class="h-8 w-10 flex items-center justify-center">${data.quantity}</div>`;
            resultsHtml += `  <a  class="h-8 w-8 text-xl flex items-center justify-center cursor-pointer select-none sumar" id="sumar" data-product-inv=${data.inventario} data-product-cant=${data.quantity}  data-product-id="${data.item}">+</a>`;
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
            resultsHtml += `                <p class="ml-4 text-indigo-600">$ ${Number(data.precio) * Number(data.quantity)}</p>`;
            resultsHtml += '               </div>';
            resultsHtml += `                 <p class="mt-2 text-sm text-gray-500">Precio ${Number(data.precio).toFixed(2)}</p>`

            resultsHtml += '             </div>';
            resultsHtml += '  <div class="flex w-28 border border-gray-300 text-gray-600 divide-x divide-gray-300 mt-5">';
            resultsHtml += `  <a  class="h-8 w-8 text-xl flex items-center justify-center cursor-pointer select-none restar" id="restar" data-product-id="${data.item}">-</a>`;
            resultsHtml += `  <div class="h-8 w-10 flex items-center justify-center">${data.quantity}</div>`;
            resultsHtml += `  <a  class="h-8 w-8 text-xl flex items-center justify-center cursor-pointer select-none sumar" id="sumar" data-product-inv=${data.inventario} data-product-cant=${data.quantity}  data-product-id="${data.item}">+</a>`;
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
    var inventioProducto=$(this).data("product-inv")
    var cantidadAgregada=$(this).data("product-cant")
    if(cantidadAgregada>=inventioProducto){
      var elemento = document.getElementById("toasterrorCarrito");
  
      // Asigna un nuevo texto al elemento
      elemento.textContent = "Limite de producto Alcanzado";
      elemento.style.display = "block";
      setTimeout(function () {
      elemento.style.display = "none";
      }, 1500);
    }else{
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
    }

 
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
