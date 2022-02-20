import psycopg2
from app.configUtil import ConfigConnect


class DbConnect:
    def __init__(
        self,
    ):
        cp = ConfigConnect()
        dict = cp.get_section_config("DB")

        self.database = dict["database"]
        self.user = dict["user"]
        self.password = dict["password"]
        self.host = dict["host"]
        self.port = dict["port"]

        self.schema = dict["schema"]
        self.tableName = None

        self.conn = None
        self.cursor = None

        pass

    def createConnection(
        self,
    ):
        if self.conn == None:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
        else:
            if self.conn.closed == 1:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                )
        print("\nConnection Established...\n")
        self.__createCursor()

    def setTableName(
        self,
        tableName,
    ):
        self.tableName = tableName
        print("\nTable Name Changed to {}\n".format(tableName))

    def setSchema(
        self,
        schema,
    ):
        self.schema = schema
        print("\nSchema Changed to {}\n".format(schema))

    def __createCursor(
        self,
    ):
        self.cursor = self.conn.cursor()
        print("\nCursor Created...\n")

    def chechExistance(
        self,
        columnName,
        columnValue,
    ):
        query = (
            "select COUNT(*) from "
            + self.schema
            + "."
            + self.tableName
            + " where "
            + str(columnName)
            + " = %s"
        )
        self.cursor.execute(query, (columnValue,))
        row = self.cursor.fetchone()
        print("\nRecord Fetched Successfully...\n")
        if row[0] == 0:
            return False
        return True

    def fetchOne(
        self,
        columnList,
        primaryKey,
        pkValue,
    ):
        query = (
            "select "
            + ",".join(columnList)
            + " from "
            + self.schema
            + "."
            + self.tableName
            + " where "
            + str(primaryKey)
            + " = %s"
        )
        self.cursor.execute(query, (pkValue,))
        row = self.cursor.fetchone()
        print("\nRecord Fetched Successfully...\n")
        return row

    def fetchMultiple(
        self,
        columnList,
        primaryKey,
        pkValue,
        orderBy=None,
    ):
        query = (
            "select "
            + ",".join(columnList)
            + " from "
            + self.schema
            + "."
            + self.tableName
            + " where "
            + str(primaryKey)
            + " = %s"
        )
        if orderBy:
            query += " order by "+str(orderBy)
        self.cursor.execute(query, (pkValue,))
        row = self.cursor.fetchall()
        print("\nRecords Fetched Successfully...\n")
        return row

    """
    conditions_dict = {
        "columnName" : columnValue,
        "columnName" : columnValue,
    }
    """

    def fetchWithMultipleCondition(self, columnList, conditions_dict, orderBy="id"):
        conditions_list = list(conditions_dict.keys())
        query = str(
            "select "
            + ",".join(columnList)
            + " from "
            + self.schema
            + "."
            + self.tableName
            + " where "
            + "AND ".join(["{} = %s "] * len(conditions_list))
            + " ORDER BY "
            + str(orderBy)
        ).format(*conditions_list)
        print(query)
        self.cursor.execute(query, (list(conditions_dict.values())))
        row = self.cursor.fetchall()
        print("\nRecords Fetched Successfully...\n")
        return row

    def updateRecord(
        self,
        updateColumn,
        updateValue,
        primaryKey,
        pkValue,
    ):
        query = (
            "update "
            + self.schema
            + "."
            + self.tableName
            + " SET "
            + str(updateColumn)
            + " = %s"
            + " where "
            + str(primaryKey)
            + " = %s"
        )
        self.cursor.execute(
            query,
            (
                updateValue,
                pkValue,
            ),
        )
        self.conn.commit()
        count = self.cursor.rowcount
        print("\n" + str(count) + " Record Updated successfully...\n")

    def insertRecord(
        self,
        columnList,
        columnValues,
    ):
        query = (
            "insert into "
            + self.schema
            + "."
            + self.tableName
            + " ("
            + ",".join(columnList)
            + ") VALUES ("
            + ",".join(["%s"] * len(columnList))
            + ")"
        )
        self.cursor.executemany(query, (columnValues,))
        self.conn.commit()
        print("\nRecord Inserted successfully...\n")

    def insertRecords(
        self,
        columnList,
        valuesList,
    ):
        query = (
            "insert into "
            + self.schema
            + "."
            + self.tableName
            + " ("
            + ",".join(columnList)
            + ") VALUES ("
            + ",".join(["%s"] * len(columnList))
            + ")"
        )
        self.cursor.executemany(query, (valuesList))
        self.conn.commit()
        count = self.cursor.rowcount
        print("\n" + str(count) + " Record Inserted successfully...\n")

    def insertRecordOneByOne(
        self,
        columnList,
        valuesList,
    ):
        query = (
            "insert into "
            + self.schema
            + "."
            + self.tableName
            + " ("
            + ",".join(columnList)
            + ") VALUES ("
            + ",".join(["%s"] * len(columnList))
            + ")"
        )
        for value in valuesList:
            self.cursor.executemany(query, (value,))
        self.conn.commit()
        print("\nRecord Inserted successfully...\n")

    def updateRecord(self, updateColumn, updateValue, primaryKey, pkValue):
        query = (
            "update "
            + self.schema
            + "."
            + self.tableName
            + " SET "
            + str(updateColumn)
            + " = %s"
            + " where "
            + str(primaryKey)
            + " = %s"
        )
        self.cursor.execute(
            query,
            (
                updateValue,
                pkValue,
            ),
        )
        self.conn.commit()
        count = self.cursor.rowcount
        print("\n" + str(count) + " Record Updated successfully...\n")

    def updateMultipleColumns(
        self, updateColumnList, updateValues, primaryKey, pkValue
    ):
        count = 0
        query = "update " + self.schema + "." + self.tableName + " SET "
        for j in range(len(updateColumnList) - 1):
            query += str(updateColumnList[j]) + "=%s , "
        query += (
            str(updateColumnList[-1])
            + "=%s WHERE "
            + str(primaryKey)
            + " = "
            + str(pkValue)
        )
        self.cursor.execute(query, (updateValues))
        count += 1
        self.conn.commit()
        print("\n" + str(count) + " Record Updated successfully...\n")

    def __closeCursor(
        self,
    ):
        self.cursor.close()
        print("\nCursor Closed...\n")

    def closeConnection(
        self,
    ):
        if self.cursor.closed == False:
            self.__closeCursor()
        if self.conn.closed == 0:
            self.conn.close()
        print("\nConnection Closed...\n")
