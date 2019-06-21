import teslajson
import vars
c = teslajson.Connection(vars.USERID, vars.PASS)
v = c.vehicles[0] # vehicles is an array. This assumes you only have one Tesla
ret = v.wake_up()
print "API Version:", ret["response"]["api_version"]
data = v.data_request('drive_state')
print "Longitude:", data["longitude"]
print "Latitude:", data["latitude"]
