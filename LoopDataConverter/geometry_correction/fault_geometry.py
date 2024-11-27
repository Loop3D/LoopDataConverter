# internal imports
from ..utils import calculate_vector_along_line, calculate_angle

#external imports
import numpy
import geopandas
import shapely


class FaultConnector:
    
    
    def __init__(self, data: geopandas.GeoDataFrame):
        self._data = data.copy()
        self.processed_data = None
        
    def connect_faults(self):
        
        """Process the GeoDataFrame to merge faults based on the angle criterion."""
        
        self.processed_data = self._data.copy()
        i = 0

        while i < len(self.processed_data):
            j = i + 1
            while j < len(self.processed_data):
                line1 = self.processed_data.iloc[i].geometry
                line2 = self.processed_data.iloc[j].geometry

                # Find the intersection
                intersection = line1.intersection(line2)
                if intersection.is_empty or not intersection.geom_type == "Point":
                    j += 1
                    continue  # Skip if no intersection or if it's not a point
                
                # Get the intersection point
                intersection_point = numpy.array(intersection.coords[0])

                # Compute vectors aligned with each LineString
                vector1 = calculate_vector_along_line(line1, intersection_point)
                vector2 = calculate_vector_along_line(line2, intersection_point)

                # Ensure non-zero vectors before proceeding
                if numpy.linalg.norm(vector1) == 0 or numpy.linalg.norm(vector2) == 0:
                    j += 1
                    continue

                # Calculate the angle between the vectors
                angle = calculate_angle(vector1, vector2)

                # If the angle is below 20 degrees, merge the lines
                if angle < 20:
                    merged_line = shapely.geometry.LineString(list(line1.coords) + list(line2.coords))

                    # Add the merged line and remove the old ones
                    self.processed_data = self.processed_data.drop([i, j]).reset_index(drop=True)
                    self.processed_data = self.processed_data.append({'geometry': merged_line}, ignore_index=True)

                    # Restart processing for safety (to avoid index shifts)
                    i = 0
                    j = 0
                else:
                    j += 1  # Move to the next line

            i += 1
        
    