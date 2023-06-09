var btns = document.getElementsByClassName("update-cart");
// console.log("Hello World",user,btns);

for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function () {
        var prodId = this.dataset.product
        var action = this.dataset.action
        console.log("pid", prodId, "action",action);

        if (user === 'AnonymousUser') {
            console.log("User is not authenticated")
            addCookieItem(prodId,action);
        }
        else
        {
            updateCart(prodId, action);
        }
    })
}

function addCookieItem(productId,action)
{
    if (action=='add')
    {
        if (cart[productId]==undefined)
        {
            cart[productId] = {'quantity':1}
        }
        else
        {
            cart[productId]['quantity'] +=1
        }
    }
    else if(action=='remove')
    {
        if(cart[productId]['quantity']==1)
        {
            console.log(cart[productId],"cart item removed")
            delete cart[productId] 
        }
        else
        {
            cart[productId]['quantity']-=1;
        }
    }
    console.log("addCookieItem",cart);
    document.cookie = "cart="+JSON.stringify(cart)+";domain=;path=/"
    location.reload();
}


function updateCart(prodId, action) {
    var url = '/update_item/'
    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': prodId, 'action': action })

    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log("Data:", data)
            location.reload();
        });
}
