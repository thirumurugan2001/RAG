from rag import *

# This AzureOpenAIController function is use to Validate the payload data["prompt"] is not empty and string format.
def ragController(Question):
    try:
        if Question != "":
            return rag(Question)
        else:
            return {
                "message":"Invaild data !",
                "statusCode":400
            }
    except Exception as e:
        print(f"Error in ragController controller.py file: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400
            }