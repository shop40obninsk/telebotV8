import sqlite3 as sql
import os
def explorer_worker(path):
    directory_list = list()
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name).replace("\\", "/") + "/")
    return directory_list

def read_txt(path,mass=False):
    if not mass:
        with open(path,"r",encoding="utf-8") as f:
            f=f.read()
            return f
    else:
        with open(path,"r",encoding="utf-8") as f:
            mass= f.readlines()
        mass=[i.replace("\n","") for i in mass]
        return mass

class DataBase:
    def __init__(self,path):
        self.con = sql.connect(path)

    def add(self,table_name,column_names,mass):
        try:
            column_n=""
            for i in column_names:
                column_n+=f"{str(i)}, "
            column_n= column_n[:-2]

            values=""
            for i in mass:
                values+=f"'{str(i)}', "
            values=values[:-2]

            command= f"""INSERT INTO {str(table_name)} ({column_n}) VALUES ({values})"""
            print(command)
            cur = self.con.cursor()
            cur.execute(command)
            self.con.commit()
            return True

        except Exception as e:
            print(e)
            return False

    def get(self,table_name):
        try:
            cur = self.con.cursor()
            return [[j for j in i] for i in cur.execute(f'SELECT * FROM {table_name}')]
        except Exception as e:
            return None

    def get_filter(self, table, column, item):
        try:
            cur = self.con.cursor()
            response=[i for i in cur.execute(f"SELECT * FROM {table} WHERE {column}=?", (item,))]
            output=[]
            for i in response:
                mass=[]
                for j in i:
                    mass.append(j)
                output.append(mass)
            return output
        except:
            return False


    def check_in_base(self,table,column,item):
        try:
            cur = self.con.cursor()
            cur.execute(f"SELECT {column} FROM {table} WHERE {column}=?",(item,))
            f=cur.fetchone()
            return not(f is None)
        except:
            return False

    def check_in_base_basket(self, table, chat_id, type_good, manufacturer_id, good_id, taste_id):
        try:
            cur = self.con.cursor()
            cur.execute(f"SELECT * FROM {table} WHERE "
                        f"chat_id={chat_id} AND "
                        f"type={type_good} AND "
                        f"manufacturer_id={manufacturer_id} AND "
                        f"good_id={good_id} AND "
                        f"taste_id={taste_id}"
                        )
            f = cur.fetchone()
            return not (f is None), f
        except:
            return False


    def update_in_base(self,table,column,value_column,item_update,value_item_update):
        cur = self.con.cursor()
        cur.execute(f'''UPDATE {str(table)} SET {str(item_update)} = {str(value_item_update)} WHERE {str(column)} = {str(value_column)}''')
        self.con.commit()

    def delete_row(self, table, columns, items):
        s = f"DELETE FROM {str(table)} WHERE "
        for i in range(len(columns)):
            s += f"{str(columns[i])} = {str(items[i])}"
            if i != len(columns) - 1:
                s += " AND "
        print(s)
        cur = self.con.cursor()
        cur.execute(s)
        self.con.commit()

    def close(self):
        self.con.close()