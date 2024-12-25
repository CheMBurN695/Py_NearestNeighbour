#Hash Table class that will be used to store the packages and their information

class HashMap:
    def __init__(self):
        self.size = 200;
        self.map = [None] * self.size

    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    def add(self, package_ID, package):
        key_hash = self._get_hash(package_ID)
        key_value = [package_ID, package]

        if (self.map[key_hash] is None):
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == package_ID:
                    pair[1] = package
                    return True
            self.map[key_hash].append(key_value)
            return True

    def get(self, key):
        keyhash = self._get_hash(key)
        if self.map[keyhash] is not None:
            for pair in self.map[keyhash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        keyhashToDelete = self._get_hash(key)
        if self.map[keyhashToDelete] is None:
            return False
        for i in range (0, len(self.map[keyhashToDelete])):
            if self.map[keyhashToDelete][i][0] == key:
                self.map[keyhashToDelete].pop(i)
                return True