let updateBtns = document.getElementsByClassName('update-cart')
for (const updateBtn of updateBtns) {
    updateBtn.addEventListener('click', () => {
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log(productId);
        console.log(action);
        (user === 'AnonymousUser') ? alert("user not logged in") : updateUserOrder(productId,action);
    });
}

const updateUserOrder = (productId, action) => {
    console.log(`action is ${action}`);
    let url = '/update_item/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({'productId':productId, 'action':action} ),
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {
            console.log(`DATA ${data}`)
            location.reload()
        });
};
