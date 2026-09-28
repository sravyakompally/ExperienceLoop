document.getElementById("captureForm").addEventListener("submit", async (e) => {
 e.preventDefault(); const form=e.currentTarget; const result=document.getElementById("result");
 const data=Object.fromEntries(new FormData(form).entries());
 result.textContent="Saving…";
 try { const response=await fetch("/api/experiences",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
 const body=await response.json(); if(!response.ok) throw new Error(body.error||"Could not save");
 result.textContent=`${body.message} ID: ${body.experience_id} · Memory: ${body.memory.status}`;
 form.reset();
 } catch(err){result.textContent=err.message;}
});