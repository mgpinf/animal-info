let nord0 = "#2E3440";
let nord1 = "#3B4252";
let nord9 = "#81A1C1";
let merc0 = "#212529";
let merc1 = "#009688";
let nord7 = "#8FBCBB";
let box_shadow_val = "0 0 30px rgba(0, 150, 136, .8))";

function change_color(current_element, flag = true) {
    flag ? color = nord7 : color = nord9
    current_element.style["background-color"] = nord1
    current_element.style["border-color"] = nord1
    current_element.style["color"] = color
    current_element.style["box-shadow"] = box_shadow_val
}

function restore_color(current_element, flag = true) {
    flag ? color = nord7 : color = nord9
    current_element.style["color"] = nord1
    current_element.style["background-color"] = color
    current_element.style["border-color"] = color
    current_element.style["box-shadow"] = box_shadow_val
}