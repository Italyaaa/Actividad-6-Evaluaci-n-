#Función para carga de archivos unicamente .csv y .xlsx
def Funcion_1(data):
    import pandas as pd
    import os
    extension = os.path.splitext(data)[1].lower()
    #Cargar el archivo según su extensión
    if extension == '.csv':
        df = pd.read_csv(data)
        return(df)
    elif extension == '.xlsx':
        df = pd.read_excel(data)
        return(df)
    else:
        #Error desde la conzola
            raise ValueError(f'Formato de archivo no soportado: {extension}')   

#####################################################################################

#Sustitución valores PARES numéricos por método 'mean', valores IMPARES numéricas con la constante '99' y las que no sean tipo numérico, sustituir por 'Este_es_un_valor_nulo'

def Funcion_2(data):
    import pandas as pd
       # Separar columnas cuantitativas y cualitativas
    cuantitativas = data.select_dtypes(include=['float64', 'int64', 'float', 'int'])
    cualitativas = data.select_dtypes(include=['object', 'datetime', 'category'])
    
    # Procesar columnas cuantitativas
    for col in cuantitativas.columns:
        # Identificar el índice de la columna
        indice = cuantitativas.columns.get_loc(col)
        if indice % 2 == 0:  # Índice par
            cuantitativas[col] = cuantitativas[col].fillna(round(cuantitativas[col].mean(), 1))
        else:  # Índice impar
            cuantitativas[col] = cuantitativas[col].fillna(99)
    
    # Para columnas cualitativas
    cualitativas = cualitativas.fillna("Este_es_un_valor_nulo")
    
    # Unir las columnas cuantitativas y cualitativas en un dataframe final
    df_final = pd.concat([cuantitativas, cualitativas], axis=1)
    return df_final

###########################################################################################

#Identifica los valores nulos “por columna” y “por dataframe”

def Funcion_3(data):
    #Valores nulos por columna
    valores_nulos_cols = data.isnull().sum()
    #Valores nulos por dataframe
    valores_nulos_df = data.isnull().sum().sum()

    return ('Valores nulos por columna' , valores_nulos_cols,
            'Valores nnulos por dataframe', valores_nulos_df)

######################################################################################################

# Sustituye  los valores atípicos de las columnas numéricas con el método de “Rango intercuartílico”

def Funcion_4(data):
    import pandas as pd

    # Validar que el argumento sea un DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("El argumento debe ser un DataFrame de pandas.")

    # Crear una copia del DataFrame para trabajar con seguridad
    df_result = data.copy()

    # Seleccionar las columnas numéricas
    columnas_numericas = df_result.select_dtypes(include='number').columns

    for columna in columnas_numericas:
        # Calcular Q1, Q3 y el rango intercuartílico (IQR)
        Q1 = df_result[columna].quantile(0.25)
        Q3 = df_result[columna].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        # Sustituir valores atípicos por los límites
        df_result[columna] = df_result[columna].apply(
            lambda x: limite_inferior if x < limite_inferior else 
                      (limite_superior if x > limite_superior else x))
        
        return df_result
        