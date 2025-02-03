from Helper import *

# Function to get the most relevant answer from the database
def rag(Question):
    try:
        conn=dbconnection()
        cursor=conn.cursor()
        embedding = get_embedding(Question)
        select_query = """SELECT place, dot_product(vector, JSON_ARRAY_PACK("{0}")) AS score FROM famousPlacesIndia ORDER BY score DESC LIMIT 1 """.format(embedding)
        cursor.execute(select_query) 
        rows = cursor.fetchall() 
        if rows:
            return {
                "data":rows[0][0],
                "statusCode":200
            }
        else:
            return {
                "message":"No data found",
                "statusCode":400
            }
    except Exception as e:
        print(f"Error in rag function: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400
            }
