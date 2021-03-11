const $cupcakes = $('#cupcakes'),
    $submit = $('#submit'),
    $addCupcakeForm =  $('#add-cupcake-form'),
    $flavor = $('#flavor'),
    $size = $('#size'),
    $rating = $('#rating'),
    $image = $('#image');

async function showCupcakes() {
    const res = await axios.get('/api/cupcakes')
    for(cupcake of res.data.cupcakes) {
        const $cupcake = generateCupcakeMarkup(cupcake)
        $cupcakes.append($cupcake);
    };
};

function generateCupcakeMarkup(cupcake) {
    const $cupcake = $(`
        <li class="cupcake">
            <div>
                <img class="cupcake-img" src="${cupcake.image}" alt="cupcake-img">
                <p>Flavor: ${cupcake.flavor}</p>
                <p>Rating: <b>${cupcake.rating}</b></p>
                <p>Size: ${cupcake.size}</p>
            </div>
        </li>
    `)
    return $cupcake
}

async function addCupcake(evt) {
    evt.preventDefault()
    const cupcake = {
        flavor: $flavor.val(),
        size: $size.val(),
        rating: parseFloat($rating.val()),
        image: $image.val()
    };
    const res = await axios.post('/api/cupcakes', data=cupcake);
    const $cupcake = generateCupcakeMarkup(res.data.cupcake)
    $cupcakes.append($cupcake);
    $(this).trigger('reset');
}

$addCupcakeForm.submit(addCupcake)

$(function() {
    showCupcakes();
})