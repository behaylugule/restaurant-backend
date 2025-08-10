from rest_framework.renderers import JSONRenderer 

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response', None)
        request = renderer_context.get('request',None)

        status_code = response.status_code if response else 500
        if status_code ==204:
            return super().render(None, accepted_media_type,renderer_context)
        
        if status_code >= 400:
            print("Error response:", data)
            detail = data.get('detail',None)  if isinstance(data, dict)  else str(data)
            def parse_error(errors):
                if isinstance(errors, dict):
                    messages = []
                    for key, value in errors.items():
                        if isinstance(value, list):
                            value = " ".join(str(v) for v in value)
                        messages.append(f"{key}:{value}")
                        return " | ".join(messages)
                return str(errors)
            
            message = parse_error(data)

            return super().render({"success":False, 
                                   "status_code":status_code, 
                                   "message":message,
                                     "error":data,
                                     "path":request.get_full_path() if request else None
                                     }, accepted_media_type,renderer_context )
        

        return super().render({
            "success":True,
            "status_code":status_code,
            "data":data,
            "path":request.get_full_path() if request else None
          }, accepted_media_type,renderer_context)