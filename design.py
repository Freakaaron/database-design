class Design:

    # checks whether str1 is a subset of str2
    def is_subset(self, str1, str2):
        count = 0
        for char1 in str1:
            for char2 in str2:
                if(char1 == char2):
                    count += 1
        return count == len(str1)

    def is_equivalent(self, str1, str2):
        return str1 == str2

    def compute_closure(self, lhs, rhs, seed):
        closure = ""
        while(len(closure) < len(seed)):
            closure = seed
            for index in range (0, len(lhs)):
                if(self.is_subset(lhs[index], seed)
                    and not self.is_subset(rhs[index], seed)):
                    seed += rhs[index]
        return closure

    def compute_subsets(self, remaining_attributes):
        subsets = []
        size = len(remaining_attributes)

        for index1 in range(0,(1 << size)):
            subset = ""
            for index2 in range (0, size):
                if((index1 & (1 << index2)) > 0):
                    subset += remaining_attributes[index2]
            subsets.append(subset)
        return subsets

    def compute_keys(self, lhs, rhs, attributes):
        key = ''
        keys = []
        rhs_attributes = []
        remaining_attributes = []
        for index in range (0, len(rhs)):
            attrs = list(rhs[index])
            for attr in attrs:
                if(not attr in rhs_attributes):
                    rhs_attributes.append(attr)
        for attr in attributes:
            if(attr not in rhs_attributes):
                key += attr
            else:
                remaining_attributes.append(attr)
        subsets = self.compute_subsets(remaining_attributes)
        subsets = sorted(subsets, key=len)
        #print(subsets)
        size = len(key)
        #print(key)
        for index in range (0, len(subsets)):
            seed = key + subsets[index]
            current_size = len(seed)
            #print(seed)
            if(size == current_size):
                closure = self.compute_closure(lhs, rhs, seed)
                if(len(closure) == len(attributes)):
                    keys.append(seed)
            else:
                if(len(keys) > 0):
                    return keys
                else:
                    size += 1
                    closure = self.compute_closure(lhs, rhs, seed)
                    if (len(closure) == len(attributes)):
                        keys.append(seed)


    def compute_normal_forms(self, lhs, rhs, keys, attributes):

        key_attributes = ""
        for key in keys:
            for attribute in key:
                if(attribute not in key_attributes):
                    key_attributes += attribute

        non_key_attributes = ""
        for attribute in attributes:
            if(attribute not in key_attributes):
                non_key_attributes += attribute

        for index1 in range(0, len(lhs)):
            for index2 in range(0, len(lhs_attributes)):
                for index3 in range(0, len(keys)):
                    if (not self.is_equivalent(lhs[index1], keys[index3]) and self.is_subset(lhs[index1], keys[index3]) and not self.is_subset(rhs[index1], key_attributes)):
                        return "First Normal Form."



        count1 = 0
        count2 = 0
        for index1 in range(0, len(lhs)):
            for index2 in range (0, len(keys)):
                if(self.is_subset(rhs[index1], keys[index2]) and not self.is_equivalent(rhs[index1], keys[index2])):
                    count2 += 1
                    break
            for index2 in range (0, len(keys)):
                if(self.is_subset(keys[index2], lhs[index1])
                    or (self.is_subset(lhs[index1], keys[index2]) and self.is_subset(rhs[index1], key_attributes))):
                    count1 += 1
                    break

        if(count2 != 0 and count1 == len(lhs)):
            return "Third Normal Form."
        elif(count1 == len(lhs)):
            return "Boyce-Codd Normal Form."

        return "Second Normal Form."



if __name__ == '__main__':
    attributes = input("Enter the attribute(s) of the database:\n")
    fds = input("Enter the functional dependencies for the relation\n").split(" ")
    lhs = []
    rhs = []
    design = Design()
    for index1 in range(0, len(fds)):
        attrs = fds[index1].split("->")
        if(len(attrs[0]) > 1):
            lhs_attributes = list(attrs[0])
        else:
            lhs_attributes = attrs[0]
        if(len(attrs[1]) > 1):
            rhs_attributes = list(attrs[1])
        else:
            rhs_attributes = attrs[1]
        count = 0
        for index2 in range (0, len(lhs_attributes)):
            if(not lhs_attributes[index2] in attributes):
                count += 1
        for index2 in range(0, len(rhs_attributes)):
            if (not rhs_attributes[index2] in attributes):
                count += 1
        if(count == 0):
            for index in range(0, len(lhs)):
                if(attrs[0] == lhs[index] and attrs[1] == rhs[index]):
                    count += 1
        if(count == 0):
            for index in range(0, len(rhs_attributes)):
                if(design.is_subset(lhs_attributes, rhs_attributes[index])):
                    attrs[1] = attrs[1].replace(rhs_attributes[index], '')
        if(count == 0):
            lhs.append(attrs[0])
            rhs.append(attrs[1])
    size = int(input("Enter number of seeds for which you want to compute closure.\n"))
    for index in range (0, size):
        seed = input("Enter the seed for computing the closure.\n")
        if(seed == "quit"):
            break
        print("Closure of the above design: ", design.compute_closure(lhs, rhs, seed), "\n")
    #print(lhs, rhs)
    keys = design.compute_keys(lhs, rhs, attributes)
    print("Keys of the above design: ", keys, "\n")
    print("The above relation is in", design.compute_normal_forms(lhs, rhs, keys, attributes))


''' 
ABCD: A->B B->C C->D | Key(s): A | NF: 2NF | Done
ABC: A->BC | Key(s): A | NF: BCNF | Done
ABCD: A->BC B->D | Key(s): A | NF: 2NF | Done
ABCD: A->B B->C C->D D->A | Key(s): A, B, C, D | NF: BCNF | Done
ABC : A->AB A->X A->B B->C AB->C | Key(s): A | NF: 2NF | Done
ABCD : AB->C C->B AB->A | Key(s): ABD, ABC | NF: 3NF | Done
ABCD: A->B B->C C->D | Key(s): A | NF: 2NF | Done
ABCDEF: A->B B->C C->D F->E | Key(s): AF | NF: 1NF | Done
ABCD: AB->C C->D D->A | Key(s): BA, BC, BD NF: 3NF | Done
ABCD: B->C B->D | Key(s): AB | NF: 1NF | Done
ABCD: A->B B->C B->D | Key(s): A | NF: 2NF | Done
ABCD: AB->C BC->D CD->A AD->B | Key(s): AB, BC, CD, AD | NF: 3NF | Done
ABCD: A->C AB->D | Key(s): AB | NF: 1NF | Done
ABC: A->BC B->CA C->AB | Key(s): A, B, C | NF: BCNF | Done
'''