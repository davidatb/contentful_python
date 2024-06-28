# from dagster import job, op, repository
# from contentful import Client

# # Configura tu cliente de Contentful
# client = Client(
#     space_id='2buvodmc6l14',  # Sustituye 'your_space_id' por tu Space ID real
#     # Sustituye 'your_cda_token' por tu Content Delivery API token
#     access_token='10e59ed17266e43c614c5146db33c66fbbe9655597221158113f9c081b0c968e'
# )


# @op
# def get_contentful_entry(context, entry_id):
#     # Obtiene la entrada por su ID
#     entry = client.entry(entry_id)
#     # Asume que el campo que contiene el texto se llama 'copy'. Si el nombre es diferente, cámbialo aquí.
#     if 'copy' in entry.fields():
#         context.log.info(f"Contenido obtenido: {entry.fields()['copy']}")
#         return entry.fields()['copy']
#     else:
#         context.log.error("El campo 'copy' no existe en esta entrada.")
#         return "El campo 'copy' no existe en esta entrada."

# @job
# def contentful_query_job():
#     get_contentful_entry()

# @repository
# def my_repository():
#     return [contentful_query_job]

# # Para ejecutar el job manualmente con un parámetro específico
# if __name__ == "__main__":
#     result = contentful_query_job.execute_in_process(run_config={
#         "ops": {
#             "get_contentful_entry": {
#                 "inputs": {"entry_id": "4P6JZUfNuZEb13O7ER27aZ"}
#             }
#         }
#     })
#     print(result.success)


from contentful import Client
from contentful_management import Client as ManagementClient

# Configura tu cliente de Contentful
client = Client(
    space_id='2buvodmc6l14',  # Sustituye 'your_space_id' por tu Space ID real
    # Sustituye 'your_cda_token' por tu Content Delivery API token
    access_token='10e59ed17266e43c614c5146db33c66fbbe9655597221158113f9c081b0c968e'
)


def get_content_and_save(entry_id):
    # Obtiene la entrada por su ID
    entry = client.entry(entry_id)

    # Asume que el campo que contiene el texto se llama 'copy'. Si el nombre es diferente, cámbialo aquí.
    if 'copy' in entry.fields():
        content = entry.fields()['copy']
    else:
        content = "El campo 'copy' no existe en esta entrada."

    # Guarda el contenido en un archivo de texto
    with open('content_output.txt', 'w', encoding='utf-8') as file:
        file.write(content)

    print("Contenido guardado en 'content_output.txt'.")


# Llama a la función con el ID de entrada
get_content_and_save('4P6JZUfNuZEb13O7ER27aZ')



# Configuración del cliente de Contentful para escribir (CMA)
mgmt_client = ManagementClient('CFPAT-9wLnUQtOtJ2ekONvg8wLFudx_FR1pkNmEur7EEhm0wM')  # Sustituye 'tu_cma_token' con tu Content Management API token

def update_entry(entry_id, new_content):
    # Obtiene la entrada usando el cliente CDA (lectura)
    entry = client.entry(entry_id)
    
    if 'copy' in entry.fields():
        # Obtiene la entrada usando el cliente CMA (escritura)
        entry_to_update = mgmt_client.entries(space_id='2buvodmc6l14', environment_id='master').find(entry_id)
        
        # Actualiza el campo 'copy'
        entry_to_update.update({'fields': {'copy': {'en-US': new_content}}})  # Uso correcto del método update
        entry_to_update.save()
        entry_to_update.publish()
        
        print("Contenido actualizado con éxito.")
    else:
        print("El campo 'copy' no existe en esta entrada.")

# Llamada a la función con el ID de la entrada y el nuevo contenido
new_content = (
    "Los descuentos actuales estarán vigentes 28 de Mayo al 06 de Junio del 2024\n\n"
    "Algunas de las promociones son válidas únicamente en días específicos. Consulta los términos y condiciones de cada promoción."
)

update_entry('4P6JZUfNuZEb13O7ER27aZ', new_content)
