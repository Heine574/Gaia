<%
dim fname,city
fname=Request.Form("login")
city=Request.Form("password")
Response.Write("Dear " & fname & ". ")
Response.Write("Hope you live well in " & city & ".")
%>