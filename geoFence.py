from math import radians, sin, cos, sqrt, atan2


class geoFence():
    """ 
    A class is utilized to see if a latitude or longitude is within a specified area.
    
    Attributes
    ----------
    originPos : (double[])
        An array of [x,y] cordinates of the origin (home location) in latiude/longitude

    radius : (int)
        A number representing the radius of the circle in miles
    
    Methods
    -------
    is_inside(target):
        Returns boolian value wheather if target is inside the radius of the origin
    """    
    def __init__(self, _originPos, _radius):
        self.originPos = _originPos
        self.radius = _radius

    # Haversine formula to calculate distance between two lat/lon points
    def haversine(lat1, lon1, lat2, lon2):
        R = 3958.8  # Earth's radius in miles
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return R * c  # Distance in miles
    def is_inside(self, target):
        
        # Compute current the distance in miles from origin
        distance_miles = geoFence.haversine(self.originPos[0], self.originPos[1], target[0], target[1])
        # Print the distance
        #print(f"Distance: {distance_miles:.2f} miles")

        # Check if within radius
        if distance_miles > self.radius:
            return False
        return True