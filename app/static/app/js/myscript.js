$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})
// this is ajax function which executed when the class named (plus-cart) is clicked .
$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString() // this assign the value of pid from the class
    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        //every variable name down here canot be changed
        type:"GET",
        url :"/pluscart",
        data:{
            prod_id :id
        },
        success : function(data){
            console.log(data)
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
        }
    })
    
})
$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString() // this assign the value of pid from the class
    var eml = this.parentNode.children[2]
    console.log(id)
    $.ajax({
        //every variable name down here canot be changed
        type:"GET",
        url :"/minuscart",
        data:{
            prod_id :id
        },
        success : function(data){
            console.log(data)
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
        }
    })
    
})
$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString() // this assign the value of pid from the class
    var eml = this
    console.log(id)
    $.ajax({
        //every variable name down here canot be changed
        type:"GET",
        url :"/removecart",
        data:{
            prod_id :id
        },
        success : function(data){
            console.log("delete")
            
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
    
})