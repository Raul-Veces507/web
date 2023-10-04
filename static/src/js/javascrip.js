$(document).ready(function () {
    $(".add-to-cart-button").click(function () {
        // var addToCartUrl = window.addToCartUrl;
        // console.log(window.addToCartUrl);

        var product_id = $(this).data("product-id");
        var urlfinal=addToCartUrl.replace('0', product_id)
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
                } else if(data.status=='carrito') {
                    window.location.href =carrito
                    var toast = document.getElementById("toast");
                    toast.style.display = "block";
                    setTimeout(function () {
                        toast.style.display = "none";
                    }, 1500);

                    var cartCountElement = document.getElementById("cart-count");
                    if (cartCountElement) {
                        cartCountElement.textContent = cartData.cart_count;
                    }
                    
                }else{
                    alert("Error al agregar el producto al carrito");
                }
            }
        })
    })



    ////eliminar Productos del carrito






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
fetch(vercarrito)
  .then(response => response.json())
  .then(cartData => {
    if (cartData['cart_items']==''){
      window.location.href =carrito ;
    }else{

    
    modalcarrito.style.display = (modalcarrito.style.display === 'none') ? 'block' : 'none';
    var datos = cartData['cart_items'];
    var dato2=Number(cartData['total'])
    
  
      var resultsHtml ='     <div class="flow-root">';
          resultsHtml +='       <ul role="list" class="-my-6 divide-y divide-gray-200">';
            datos.forEach(function (data) {
          resultsHtml +='         <li class="flex py-6">';
          resultsHtml +='           <div class="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">';
          resultsHtml +=` <img src="https://riba.app/imgrs/THUMBS 500X500/${data.item}.jpg" alt="not found class="h-full w-full object-cover object-center" onerror="this.src='https://www.ribasmith.com/media/catalog/product/placeholder/default/watermark_4.png' ">`;
          resultsHtml +='           </div>';
          resultsHtml +='           <div class="ml-4 flex flex-1 flex-col">';
          resultsHtml +='             <div>';
          resultsHtml +='               <div class="flex justify-between text-base font-medium text-gray-900">';
          resultsHtml +='                 <h3>';
          resultsHtml +=`                   <a href="#">${data.nombre}</a>`;
          resultsHtml +='                 </h3>';
          resultsHtml +=`                <p class="ml-4">${data.total.toFixed(2)}</p>`;
          resultsHtml +='               </div>';
          resultsHtml +='             </div>';
          resultsHtml +='             <div class="flex flex-1 items-end justify-between text-sm">';
          resultsHtml +=`               <p class="text-gray-500">Qty ${data.quantity}</p>`;
          resultsHtml +='               <div class="flex">';
          resultsHtml +=                '<button type="submit" class="font-medium text-indigo-600 hover:text-indigo-500 delete-to-cart-button" data-product-id="${data.item}">Remove</button>'
          resultsHtml +='               </div>';
          resultsHtml +='             </div>';
          resultsHtml +='           </div>';
          resultsHtml +='         </li>';
        });
          resultsHtml +='       </ul>';
          resultsHtml +='     </div>';


        var resultsHtml2 ='  <p>Subtotal</p>';
            resultsHtml2 +=`   <p>$${dato2.toFixed(2)}</p>`;
           
       
          $('#modalintsub').html(resultsHtml2);
          $('#modalint').html(resultsHtml);
      }
  })
  .catch(error => {
    console.error("Error al obtener la cantidad del carrito", error);
  });
});





// Eliminar producto del carrito
// Selecciona todos los elementos con la clase "delete-to-cart-button"
document.addEventListener('DOMContentLoaded', () => {
// Seleccionar el botón de remove por su clase
var boton = document.querySelector(".delete-to-cart-button");

// Definir la función que quieres ejecutar al hacer clic
function saluda() {
alert("Hola");
}

// Agregar el evento de clic al botón y asignarle la función saluda
boton.addEventListener("click", ()=>{
  console.log('hola');
});
});

// $(".delete-to-cart-button").click(function () {
//   console.log('aaaa');
  // var product_id = $(this).data("product-id");
  // var urlfinal=urlfinaldelete.replace('0', product_id)
  // var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
  // $.ajax({
  //     url: urlfinal,
  //     method: "POST",
  //     dataType: "json",
  //     headers: {
  //         "X-CSRFToken": csrfToken  // Agrega el token CSRF como encabezado
  //     },
  //     success: function (data) {
         
  //         if (data.status === "success") {
  //             fetch(cartoCartUrl)
  //                 .then(response => response.json())
  //                 .then(cartData => {
  //                     var toast = document.getElementById("toast");
  //                     toast.style.display = "block";
  //                     setTimeout(function () {
  //                         toast.style.display = "none";
  //                     }, 1500);

  //                     var cartCountElement = document.getElementById("cart-count");
  //                     if (cartCountElement) {
  //                         cartCountElement.textContent = cartData.cart_count;
  //                     }
  //                 })
  //                 .catch(error => {
  //                     console.error("Error al obtener la cantidad del carrito", error);
  //                 });
  //             // Actualiza la interfaz de usuario según sea necesario
  //         } else if(data.status=='carrito') {
  //             window.location.href =carrito
  //             var toast = document.getElementById("toast");
  //             toast.style.display = "block";
  //             setTimeout(function () {
  //                 toast.style.display = "none";
  //             }, 1500);

  //             var cartCountElement = document.getElementById("cart-count");
  //             if (cartCountElement) {
  //                 cartCountElement.textContent = cartData.cart_count;
  //             }
              
  //         }else{
  //             alert("Error al agregar el producto al carrito");
  //         }
  //     }
  // })
// })
})