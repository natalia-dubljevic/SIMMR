import json

class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        from controller import Controller

        if isinstance(obj, Controller):
            obj_dict = {
                'user_inputs': obj.user_inputs,
                'scanner_bbox': obj.scanner.bbox,
                'scanner_vol_res': obj.scanner.vol_res,
                'coils': self.encode_coils(obj)
            }
            return obj_dict
        
        return super().default(obj)
    
    def encode_coils(self, controller):
        to_return = []
        for coil in controller.scanner.coils:
            to_append = []
            # to_append.append(self.encode_segments(coil))
            to_append.append(coil.B_vol.tolist())
            to_return.append(to_append)
        return to_return

    # def encode_segments(self, coil):
    #     to_return = []
    #     for segment in coil.segments:
    #         to_return.append([segment.low_lim, segment.up_lim])
    #     return to_return