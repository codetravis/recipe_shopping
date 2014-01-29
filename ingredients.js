
var count = 1;

function addIngredient()
{
    if (count < 9)
    {
        var list = document.getElementById('ingredient_list');
        var current_html = list.innerHTML;
        var new_ingredient = '<label>Ingredient ' + count + '</label>';
        new_ingredient += '<input name="ingredient_' + count  + '" type="text"/><br/>';
        list.innerHTML = current_html + new_ingredient;
        count += 1;
    }
    else
    {
       document.getElementById('add_ingredient').style.display = 'none'; 
    }
}

window.onload = function() {
document.getElementById('add_ingredient').onclick = addIngredient;
}
