function delete_todo(){
    if(confirm("本当に削除しますか？")){
        return true;
    }else{
        return false;
    }
}

function update_todo(update_id){
    const fields = [
        { name:"update_task", label:"新しいタスク名"},
        { name:"update_member_name", label:"新しい担当者名"},
        { name:"update_limit_date", label:"新しい期限（YYYY-MM-DD）"},
        { name:"update_note", label:"新しい備考"}
    ];

    let updateForm = document.getElementById("update_form" + update_id);
    let hasUpdate = false;

    for (let field of fields) {
        let newValue = prompt(`${field.label}を入力してください`);
        if (newValue !== null && newValue.trim() !== "") {
            let newElement = document.createElement("input");
            newElement.setAttribute("type", "hidden");
            newElement.setAttribute("name", field.name);
            newElement.setAttribute("value", newValue);
            updateForm.appendChild(newElement);
            hasUpdate = true; 
        }
    }
    return hasUpdate;
}
