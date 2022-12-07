class VirtualMachine:
    # Constructor
    def __init__(self):
        self.memory = [None, None, None]
    
    # getter untuk memory
    def get_vm_memory(self): return self.memory

    # setter untuk memory
    def set_vm_memory(self, idx, value):
        self.memory[idx] = value
    
    # method untuk membuang kurung dari string input
    def remove_braces(self, string):
        string = string.replace("(","")
        string = string.replace(")","")
        return string

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
        # input_list = ['=', '0', '*', '3', '+', '1', '2']

        # membuat list yang isinya string dari 0 - 9
        numbers = [str(i) for i in range(10)]

        # iterasi input list nya, kalo dia string 0 - 9 maka ubah jadi integer
        for i in range(len(input_list)): 
            if input_list[i] in numbers: input_list[i] = int(input_list[i])

        # input_list (yang di return) = ['=', 0, '*', 3, '+', 1, 2]
        return input_list
    
    # method untuk check apakah value di pita itu angka atau float
    def pita_value_type_is_number(self,pita_value): return True if isinstance(pita_value,int) or isinstance(pita_value,float) else False

    def calculate_polish_notation(self, pita:list, idx:int):
        """
        variabel pita_value ini isinya bisa +, -, *, /, dan semua integer dari 0 - 9
        """
        pita_value = pita[idx]
        print(pita_value,' ini pita value')
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

    def run(self, _inputs, idx=0):
        _input = _inputs[idx]
        print(f'ini input diatas {_input}')    
        while _input[0] != "end":
            if _input[0] == "=":
                memory_idx = _input[1]
                pita = []
                for x in range(2, len(_input)): pita.append(_input[x])
                value = self.calculate_polish_notation(pita, 0)
                self.set_vm_memory(memory_idx, value)
                print(self.memory)

            elif _input[0] == "goto":
                idx = _input[1]
                _input = _inputs[idx]
                continue

            elif _input[0] == "IF":
                print(f'input = {_input}')
                condition = [_input[1], _input[2], _input[3]]
                # math_symbol isinya cuman >, <, >=, <=, ==
                math_symbol = condition[0]
                next_step = []
                for i in range(4, len(_input)): next_step.append(_input[i])
                if math_symbol == ">":
                    if self.memory[condition[1]] > self.memory[condition[2]]:
                        _input = next_step
                        continue

                elif math_symbol == "<":
                    if self.memory[condition[1]] < self.memory[condition[2]]:
                        _input = next_step
                        continue

                elif math_symbol == ">=":
                    if self.memory[condition[1]] >= self.memory[condition[2]]:
                        _input = next_step
                        continue

                elif math_symbol == "<=":
                    if self.memory[condition[1]] <= self.memory[condition[2]]:
                        _input = next_step
                        continue

                elif math_symbol == "==":
                    if self.memory[condition[1]] == self.memory[condition[2]]:
                        _input = next_step
                        continue

            idx += 1
            _input = _inputs[idx]
            print(f'ini input dibawah {_input}')

def readTxtFile(txtFileName):
    with open(txtFileName) as f: theFile = f.readlines()
    return theFile

def make_clean_instructons():
    clean_instructons = []
    for line in instructions: clean_instructons+=line.split("\n")[0:-1]
    for i in range(len(clean_instructons)): clean_instructons[i] = vm.change_number_to_integer(clean_instructons[i])
    return clean_instructons

if __name__ == "__main__":
    # biar rapih aja
    print()
    vm = VirtualMachine()

    instructions = readTxtFile('./instructions/instruction-1.txt')
    # instructions = ['(start)\n', '(= 0 (* 3( + 1 2)))\n', '(= 1 (* 3( + 0 2)))\n', '(IF (> 0 1) (goto 6))\n', '(= 2 (0))\n', '(goto 7)\n', '(= 2 (1))\n', '(end)\n']
    # note: karena masih ada /n nya pas baca txt kita harus bersihin /n nya dari instructions nya makanya dibuat function make_clean_instructons

    clean_instructions = make_clean_instructons()
    # clean_instructions = ['(start)', '(= 0 (* 3( + 1 2)))', '(= 1 (* 3( + 0 2)))', '(IF (> 0 1) (goto 6))', '(= 2 (0))', '(goto 7)', '(= 2 (1))', '(end)']

    initial_memory = vm.get_vm_memory()
    print(initial_memory)
    vm.run(clean_instructions)