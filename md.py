class Markdown:
    def __init__(self,file,default=None):
        self.index = 0
        self.output = ""
        self.file_name = file
        try:
            with open(file) as f:
                self.read = f.read()+"\n"
        except OSError as e:
            if default:
                print("Creating new file")
                self.read = default+"\n"
            else:
                raise e

    # Reads until a target sub string. Returns False if not found. Otherwise returns string read.
    def read_until(self, target, output=True):
        result = ""
        while self.read[self.index:self.index+len(target)]!=target:
            result+=self.read[self.index]
            if output:
                self.output+=self.read[self.index]
            self.index+=1
            if self.index>=len(self.read):
                return False
        return result
    
    # Reads until end
    def read_until_end(self, output=True):
        while self.index<len(self.read):
            if output:
                self.output+=self.read[self.index]
            self.index+=1
    
    # Reads a md table. Returns list of rows or None.
    def read_table(self, row_types):
        if not self.read_until("|"):
            print("No table")
            return None
        rows = []
        row_index = 0
        
        while self.read[self.index] == "|":
            self.index+=1
            row = []
            col = 0
            for t in row_types:
                v = self.read_until("|", output=False).strip()
                if row_index==0:
                    row.append(v)
                elif row_index>1:
                    if len(v)==0 and t[1]!=False:
                        row.append(t[1])
                    elif v.lower()=="none" and t[1]==None:
                        row.append(None)
                    else:
                        try:
                            row.append(t[0](v))
                        except ValueError as e:
                            raise ValueError(f"Value '{v}' in row: {row_index} col: {col} should be of type '{t[0]}'. There was no default value. Error:\n{e}")
                self.index+=1
                col+=1
            if not row_index==1:
                rows.append(row)
            self.index+=1
            row_index+=1
        return rows
        
    def write_table(self, rows):
        max_len = [0 for i in rows[0]]
        for row_index in range(len(rows)):
            for col in range(len(rows[row_index])):
                if type(rows[row_index][col])==float:
                    rows[row_index][col] = f"{rows[row_index][col]:.2f}"
                else:
                    rows[row_index][col] = str(rows[row_index][col])
                if len(rows[row_index][col])>max_len[col]:
                    max_len[col] = len(rows[row_index][col])
        for row_index in range(len(rows)):
            for col in range(len(rows[row_index])):
                r = rows[row_index][col] + " "*(max_len[col] - len(rows[row_index][col]))
                self.output+=f"| {r} "
            if row_index == 0:
                self.output+="|\n"
                for col in range(len(rows[row_index])):
                    r = "-"*max_len[col]
                    self.output+=f"| {r} "
            self.output+="|\n"
    def write_file(self):
        self.read_until_end()
        with open(self.file_name, "w") as f:
            f.write(self.output)
        print("\n\nWritten File")
