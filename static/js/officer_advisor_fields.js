function dynamicOfficers(val) {
	// Container <div> where dynamic content will be placed
    var container = document.getElementById("holder");
    // Clear previous contents of the container
    while (container.hasChildNodes()) {
        container.removeChild(container.lastChild);
    }
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
