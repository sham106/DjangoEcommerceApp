console.log('hello')
var updateBtns = document.getElementsByClassName('update-cart')

// loop through all the buttons
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log('USER:', user)

        if (user == 'AnonymousUser') {
            console.log('user is not authenticated')
        } else {
            updateUserOrder(productId, action)
        }
    })
}
function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...')

    var url = '/update_item/'

    fetch(url, {

        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json();
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        });
}

function addCookieItem(productId, action) {
    console.log('User is not authenticated')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }

        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted')
            delete cart[productId];
        }
    }
    console.log('CART:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}


//search functionality
const search = () => {
    //get values from user
    const searchbox = document.getElementById("form-control").value.toUpperCase();
    //match input with the product list
    const storeItems = document.getElementById("row")
    const product = document.querySelectorAll(".col-lg-4")
    const pname = storeItems.getElementsByTagName("h6")

    for (var i = 0; i < pname.length; i++) {
        let match = product[i].getElementsByTagName('h6')

        if (match) {
            let textvalue = match.textcontent || match.innerHTML
            if (textvalue.toUpperCase().indexof(searchbox) > -1) {
                product[i].style.display = "";
            } else {
                product[i].style.display = "none";
            }
        }
    }
}