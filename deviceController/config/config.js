const domain = 'http://101.34.100.50'
const port = '8000'
const UserURL = domain +':' + port + '/'+ 'user/'
const DeviceURL = domain +':' + port + '/'+ 'iot/'
var url = {
	'UserURL':UserURL,
	'DeviceURL':DeviceURL
}
 
 
export {url}