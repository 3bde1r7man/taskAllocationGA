import random

class TaskAllocation:
    def __init__(self, file):
        self.file = file
        self.test_cases_number = 0
        self.data = []
        self.GENERATIONS = 400
        self.POPULATION_SIZE = 100
        self.MUTATION_PROB = 0.01
        self.CROSSOVER_PROB = 0.5
        self.read_file()

    def read_file(self):
        with open(self.file) as f:
            self.test_cases_number = int(f.readline())
            for i in range(self.test_cases_number):
                max_time = int(f.readline())
                tasks = int(f.readline())
                task_list = []
                for j in range(tasks):
                    task = f.readline()
                    task_list.append(int(task))
                self.data.append((max_time, tasks, task_list))
        f.close()

    def generate_population(self, size, test_case_number):
        population = []
        for i in range(size):
            chromosome = []
            for j in range(self.data[test_case_number][1]):
                chromosome.append(random.randint(0, 1))
            population.append(chromosome)
        return population
    
    def fitness(self, chromosome, test_case_number):
        core1 = 0
        core2 = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                core1 += self.data[test_case_number][2][i]
            else:
                core2 += self.data[test_case_number][2][i]
        max_exe = max(core1, core2)
        if max_exe > self.data[test_case_number][0]:
            return float("inf")
        else:
            return max_exe

    
    def roulette_wheel_selection(self, population, test_case_number):
        fitness_values = []
        for chromosome in population:
            fitness_values.append(self.fitness(chromosome, test_case_number))   

        inverted_fitness = []
        for f in fitness_values:
            if f != float("inf"):
                inverted_fitness.append(1 / f)
            else:
                inverted_fitness.append(1e-6)

        total_inverted_fitness = sum(inverted_fitness)

        selection_probs = []
        for f in inverted_fitness:
            if f != float("inf"):
                selection_probs.append(f / total_inverted_fitness)
            else:
                selection_probs.append(1e-6)

        cumulative_probs = []
        cumulative_sum = 0
        
        for prob in selection_probs:
            cumulative_sum += prob
            cumulative_probs.append(cumulative_sum)

        rand_num = random.random()
        for i, cumulative_prob in enumerate(cumulative_probs):
            if rand_num <= cumulative_prob:
                return population[i]
            

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return child1, child2
    
    def mutation(self, chromosome, mutation_prob):
        for gene in chromosome:
            if random.random() <= mutation_prob:
                chromosome[gene] = 1 - chromosome[gene]
            else:
                chromosome[gene] = chromosome[gene]
        return chromosome
    
    def elitism_replacment(self, population, new_population, test_case_number):
        best_chromosome = max(population, key=lambda x: self.fitness(x, test_case_number))
        best_chromosome_new = min(new_population, key=lambda x: self.fitness(x, test_case_number))
        
        if self.fitness(best_chromosome_new, test_case_number) < self.fitness(best_chromosome, test_case_number):
            population.remove(best_chromosome)
            population.append(best_chromosome_new)
        
        return population
    
    def genetic_algorithm(self, test_case_number, population_size, mutation_prob, crossover_prob, generations): 
        population = self.generate_population(population_size, test_case_number)
        for generation in range(generations):
            new_population = []
            for i in range(population_size // 2):
                
                parent1 = self.roulette_wheel_selection(population, test_case_number)
                parent2 = self.roulette_wheel_selection(population, test_case_number)
                r2 = random.random()
                if r2 > crossover_prob:
                    child1, child2 = parent1, parent2
                else:
                    child1, child2 = self.crossover(parent1, parent2)
                
                child1 = self.mutation(child1, mutation_prob)
                child2 = self.mutation(child2, mutation_prob)
                
                new_population.append(child1)
                new_population.append(child2)
            
            population = self.elitism_replacment(population, new_population, test_case_number)
        
        best_chromosome = min(population, key=lambda x: self.fitness(x, test_case_number))
        return best_chromosome, self.fitness(best_chromosome, test_case_number)
    
    def run(self):
        for i in range(self.test_cases_number):
            best_chromosome, best_fitness = self.genetic_algorithm(i, self.POPULATION_SIZE, self.MUTATION_PROB, self.CROSSOVER_PROB, self.GENERATIONS)
            print(f"Test case {i + 1}:")
            print(f"Best solution: {best_chromosome}")
            print(f"Fitness: {best_fitness}")
            print(f"Tasks assigned to core 1: {[self.data[i][2][j] for j in range(len(best_chromosome)) if best_chromosome[j] == 1]}")
            print(f"Tasks assigned to core 2: {[self.data[i][2][j] for j in range(len(best_chromosome)) if best_chromosome[j] == 0]}")
            print(f"Total time: {best_fitness}")
            print("-"*50)
            

if __name__ == "__main__":
    task_allocation = TaskAllocation("input.txt")
    task_allocation.run()

# Directed by: Ahmed Hanfy, Abdelrhman Mostafa, Marwan Tarek