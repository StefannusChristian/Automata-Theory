from prettytable import PrettyTable,ALL
class VirtualMachine:
    # Constructor
    def __init__(self):
        self.memory = [None, None, None]
    
    # getter untuk memory
    def get_vm_memory(self): return self.memory

    # setter untuk memory
    def set_vm_memory(self, idx, value):
        try: self.memory[idx] = value
        except: 
            print("\nERROR!")
            print("Possible Error: Invalid Polish Notation!\n")
        
    # method untuk membuang kurung dari string input
    def remove_braces(self, string): return string.replace("(","").replace(")","")

    """
    fungsi untuk ubah angka yang berupa string di txt ke int
    karena kalau read dari txt otomatis 2 akan dibaca sebagai "2" dan 
    string gabisa dilakukan operasi matematika jadi string 0 - 9 harus diubah jadi int
    """
    def change_number_to_integer(self, string):
        """ 
        kurung () harus dibuang dari input dan input nya ini harus dibuat menjadi list 
        setelah dibuang kurung nya hasilnya akan menjadi `= 0 * 3 + 1 2`
        """
        no_braces_string = self.remove_braces(string)
        input_list = no_braces_string.split(" ")
        """ 
        input_list = ['=', '0', '*', '3', '+', '1', '2']
        """
        
        # Remove empty spaces from string list
        input_list = list(filter(None, input_list))

        """ 
        iterasi input list nya, kalo string nya bisa langsung di convert ke integer berarti dia angka
        kalo gabisa berarti dia bukan 0 - 9 jadi kita pass aja
        """
        for i in range(len(input_list)): 
            try: input_list[i] = int(input_list[i])
            except: pass
        
        # input_list (yang di return) = ['=', 0, '*', 3, '+', 1, 2]
        return input_list
    
    # method untuk check apakah value di pita itu angka atau float
    def pita_value_type_is_number(self,pita_value): return True if isinstance(pita_value,int) or isinstance(pita_value,float) else False

    def calculate_polish_notation(self, pita:list, idx:int):
        """
        variabel pita_value ini isinya bisa +, -, *, /, dan semua integer dari 0 - 9
        """
        pita_value = pita[idx]
        """
        Contoh recursion untuk input [0, '*', 3, '+', 1, 2]:
        a,b = 1,2
        a,b = 3,3
        output = 9
        """
        if self.pita_value_type_is_number(pita_value): return pita_value
        else:
            a = self.calculate_polish_notation(pita, idx + 1)
            b = self.calculate_polish_notation(pita, idx + 2)

            # pita nya baca +
            if pita_value == "+": return a + b
            
            # pita nya baca -
            elif pita_value == "-": return a - b

            # pita nya baca *
            elif pita_value == "*": return a * b

            # pita nya baca /
            elif pita_value == "/": return a / b

    def run(self, instructions, instruction_ke, idx=0):
        step = instructions[idx]
        print(f'{instructions}')
        while step[0] != "end":
            print(f'\nJalankan line {idx}:')
            print(f'step =  {step}')    
            if step[0] == "start": print(f'Memory = {self.get_vm_memory()}')
            elif step[0] == "=":
                """
                step =  ['=', 0, '*', 3, '+', 1, 2]
                """
                memory_idx = step[1]

                """
                pita itu buat ambil polish notation nya aja 
                """
                pita = step[2:]
                # pita = ['*', 3, '+', 1, 2]
                # hitung hasil dari polish notation
                value = self.calculate_polish_notation(pita, 0)
                
                # set memory di index ke idx dengan value 
                self.set_vm_memory(memory_idx, value)
                print(f'Memory = {self.get_vm_memory()}')
            
            elif step[0] == "M":
                # pita = ['M', '=', 2, 1]
                memory_idx = step[2]
                # operator isinya cuman +, *, /, - , =
                operator = step[1]
                if operator == "=": value = self.get_vm_memory()[step[3]]
                elif operator == "+":
                    if self.get_vm_memory()[memory_idx] is None:
                        self.get_vm_memory()[memory_idx] = 0
                        value = self.get_vm_memory()[memory_idx] + self.get_vm_memory()[step[3]]
                elif operator == "-":
                    if self.get_vm_memory()[memory_idx] is None:
                        self.get_vm_memory()[memory_idx] = 0
                        value = self.get_vm_memory()[memory_idx] - self.get_vm_memory()[step[3]]
                elif operator == "*":
                    if self.get_vm_memory()[memory_idx] is None:
                        self.get_vm_memory()[memory_idx] = 0
                        value = self.get_vm_memory()[memory_idx] * self.get_vm_memory()[step[3]]
                elif operator == "/":
                    if self.get_vm_memory()[memory_idx] is None:
                        self.get_vm_memory()[memory_idx] = 0
                        value = self.get_vm_memory()[memory_idx] / self.get_vm_memory()[step[3]]

                self.set_vm_memory(memory_idx, value)
                print(f'Memory = {self.get_vm_memory()}')

            elif step[0] == "goto":
                # step = ["goto",6]
                
                """ 
                kalau udh masuk sini step itu isinya cuman goto<step-berapa>
                """
                # ambil index pengen pergi ke step berapa
                idx = step[1]
                step = instructions[idx]
                print(f'Memory = {self.get_vm_memory()}')
                if step[0] == "end":
                    print(f'\nJalankan line {idx}:')
                    print(f'step = {step}') 
                    print(f'Memory = {self.get_vm_memory()}')
                    print(f"\nINSTRUCTION {instruction_ke} FINISHED!")
                continue

            elif step[0] == "IF":
                print(f'Memory = {self.get_vm_memory()}')
                # ['IF', '>', 0, 1, 'goto', 6]
                condition = [step[1], step[2], step[3]]
                # math_symbol isinya cuman >, <, >=, <=, ==
                math_symbol = condition[0]

                # next bakal simpan ["goto","6"]
                next_step = step[4:]
                if self.get_vm_memory()[condition[1]] is None: self.get_vm_memory()[condition[1]] = 0
                if self.get_vm_memory()[condition[2]] is None: self.get_vm_memory()[condition[2]] = 0
                if math_symbol == ">":
                    if self.get_vm_memory()[condition[1]] > self.get_vm_memory()[condition[2]]:
                        step = next_step
                        continue

                elif math_symbol == "<":
                    if self.get_vm_memory()[condition[1]] < self.get_vm_memory()[condition[2]]:
                        step = next_step
                        continue

                elif math_symbol == ">=":
                    if self.get_vm_memory()[condition[1]] >= self.get_vm_memory()[condition[2]]:
                        step = next_step
                        continue

                elif math_symbol == "<=":
                    if self.get_vm_memory()[condition[1]] <= self.memory[condition[2]]:
                        step = next_step
                        continue

                elif math_symbol == "==":
                    if self.memory[condition[1]] == self.memory[condition[2]]:
                        step = next_step
                        continue

            idx += 1
            try:
                step = instructions[idx]
            except: 
                print("\nERROR!")
                print("Possible Error: Typo in input!\n")
                break

            print(f'next step adalah line {idx}: {step}')
            if step[0] == "end":
                print(f'\nJalankan line {idx}:')
                print(f'step = {step}') 
                print(f'Memory = {self.get_vm_memory()}')
                print(f"\nINSTRUCTION {instruction_ke} FINISHED!")

def readTxtFile(txtFileName):
    with open(txtFileName) as f: theFile = f.readlines()
    return theFile

def make_clean_instructons():
    clean_instructons = []
    for line in instructions: clean_instructons+=line.split("\n")[0:-1]
    for i in range(len(clean_instructons)): clean_instructons[i] = vm.change_number_to_integer(clean_instructons[i])
    return clean_instructons

def print_instructions(instructions,instruction_ke,step=0):
    instruction_table = PrettyTable(["Line","Instruction"])
    instruction_table.title = f"INSTRUCTION {instruction_ke}"
    instruction_table.hrules=ALL
    for line in instructions: 
        step = str(step)+":"
        instruction_table.add_row([step,line])
        step = int(step[:-1])
        step+=1
    return instruction_table

if __name__ == "__main__":
    user_input = input("\nRun Instruction Ke: ")
    vm = VirtualMachine()

    instructions = readTxtFile(f'./instructions/instruction-{user_input}.txt')
    # instructions = ['(start)\n', '(= 0 (* 3( + 1 2)))\n', '(= 1 (* 3( + 0 2)))\n', '(IF (> 0 1) (goto 6))\n', '(= 2 (0))\n', '(goto 7)\n', '(= 2 (1))\n', '(end)\n']
    # note: karena masih ada /n nya pas baca txt kita harus bersihin /n nya dari instructions nya makanya dibuat function make_clean_instructons

    instructions_table = print_instructions(instructions,user_input)
    print(instructions_table)

    clean_instructions = make_clean_instructons()
    # clean_instructions = ['(start)', '(= 0 (* 3( + 1 2)))', '(= 1 (* 3( + 0 2)))', '(IF (> 0 1) (goto 6))', '(= 2 (0))', '(goto 7)', '(= 2 (1))', '(end)']

    initial_memory = vm.get_vm_memory()
    print(f"\nSTART INSTRUCTION {user_input}!\n")
    print(f"Initial Memory = {initial_memory}")
    vm.run(clean_instructions,user_input)