function dynamicOfficers(val) {
	// Container <div> where dynamic content will be placed
    var container = document.getElementById("holder");
    // Clear previous contents of the container
    while (container.hasChildNodes()) {
        container.removeChild(container.lastChild);
    }
    //var newContainer = document.createElement("Fieldset");
    container = container.appendChild(document.createElement("Fieldset"));
    
    for (i=0;i<val;i++){
        // Append a node with a random text
        container.appendChild(document.createTextNode("Officer " + (i+1)));
        container.appendChild(document.createElement("br"));
        // Create an <input> element, set its type and name attributes
    
    	
        var name = document.createElement("input");
        name.id = "off_name" + i;
        name.type = "text";
        name.name = "off_name" + i;
        var label = document.createElement("LABEL");
    	label.htmlFor = "off_name" + i;
        label.innerHTML="Officer Name " + (i+1);
        container.appendChild(label);
        container.appendChild(name);
        container.appendChild(document.createElement("br"));
        
        container.appendChild(document.createTextNode("Officer Phone " + (i+1)));
        var phone = document.createElement("input");
        phone.type = "text";
        phone.name = "off_phone" + i;
        container.appendChild(phone);
        container.appendChild(document.createElement("br"));
        
        container.appendChild(document.createTextNode("Officer Email " + (i+1)));
        var email = document.createElement("input");
        email.type = "text";
        email.name = "off_email" + i;
        container.appendChild(email);
        container.appendChild(document.createElement("br"));
        
        container.appendChild(document.createTextNode("Officer Position " + (i+1)));
        var pos = document.createElement("input");
        pos.type = "text";
        pos.name = "off_pos" + i;
        container.appendChild(pos);
        
        // Append a line break 
        container.appendChild(document.createElement("br"));
    }
}
    	
function dynamicAdvisors(val) {
	// Container <div> where dynamic content will be placed
    var container = document.getElementById("advisor_form");
    // Clear previous contents of the container
    while (container.hasChildNodes()) {
        container.removeChild(container.lastChild);
    }
    for (i=0;i<val;i++){
        // Append a node with a random text
        container.appendChild(document.createTextNode("Advisor " + (i+1)));
        container.appendChild(document.createElement("br"));
        // Create an <input> element, set its type and name attributes
    
    	
        var name = document.createElement("input");
        name.id = "adv_name" + i;
        name.type = "text";
        name.name = "adv_name" + i;
        var label = document.createElement("LABEL");
    	label.htmlFor = "adv_name" + i;
        label.innerHTML="Advisor Name " + (i+1);
        container.appendChild(label);
        container.appendChild(name);
        container.appendChild(document.createElement("br"));
        
        container.appendChild(document.createTextNode("Advisor Phone " + (i+1)));
        var phone = document.createElement("input");
        phone.type = "text";
        phone.name = "adv_phone" + i;
        container.appendChild(phone);
        container.appendChild(document.createElement("br"));
        
        container.appendChild(document.createTextNode("Advisor Email " + (i+1)));
        var email = document.createElement("input");
        email.type = "text";
        email.name = "adv_email" + i;
        container.appendChild(email);
        container.appendChild(document.createElement("br"));
        
        // Append a line break 
        container.appendChild(document.createElement("br"));
    }
}

function removeFieldset(e) {
	var fieldset = e.parentNode;
	var container = fieldset.parentNode;
	var inputs = fieldset.getElementsByTagName("input");
	var cur_idx = parseInt(inputs[0].name.slice(-1));
	e.parentNode.parentNode.removeChild(e.parentNode);
	
	
	//Decrement add button
	var addButton = container.nextElementSibling;
	var id = parseInt(addButton.id);
	addButton.id = (id-1).toString();
	
	//Decerement all lower fieldsets
    var inputs = container.getElementsByTagName("input");
    for(let i=0; i<inputs.length; i++) {
    	var name = inputs[i].name;
    	var idx = parseInt(name.slice(-1));
    	if (idx > cur_idx) {
    		idx -= 1;
			name = name.slice(0, -1) + idx.toString();
			inputs[i].name = name;
		}
    }
    
   //Decrement num_officer counter
   var num_member_ctr = container.previousElementSibling;
   num_member_ctr.value = parseInt(num_member_ctr.value) - 1;
}

function addMemberFieldset(button) {
	var i = parseInt(button.id);
	var container = button.previousElementSibling;
	var form = container.children[0];
	var newForm = form.cloneNode(true);

    container.appendChild(newForm);
    var newid = i + 1;
    var inputs = newForm.getElementsByTagName("input");
    for(let i=0; i<inputs.length; i++) {
    	var name = inputs[i].name;
    	name = name.slice(0, -1) + newid.toString();
    	inputs[i].name = name;
    	inputs[i].value = null;
    }
    var removeButton = newForm.getElementsByTagName("button")[0];
    removeButton.style = "position: absolute;right:10px;top:-5px;outline:5px solid #fff";
    
    //Increment the counter of the add button
    button.id = newid.toString();
    //Increment the counter of num_officers
    var num_member_ctr = document.getElementById("num_members");
    num_member_ctr.value = newid +1;
    
}
