import matlab.engine


class MLC3(object):
    def __init__(self):
        self.eng = matlab.engine.start_matlab()
        # Add path
        self.eng.addpath("./matlab_code")
        self.eng.addpath("./matlab_code/MLC_tools")
        self.eng.addpath("./matlab_code/MLC_tools/Demo")

        self.mlc = self.eng.MLC2()
        self.params = self.eng.get_params(self.mlc)

        self.eng.workspace["wparams"] = self.params
        self.table = self.eng.MLCtable(self.eng.eval("wparams.size")*50)
        self.eng.set_table(self.mlc, self.table)

        # print "Selection method: " + self.eng.eval("wparams.selectionmethod")

        # self.eng.workspace["wtable"] = self.table
        # print "Table number: " + self.eng.eval("wtable.number")

    def go(self, ngen, fig):
        # self.eng.go(self.mlc, generations, fig

        if ngen <= 0:
            print('Once you tell me how I can compute %f generations, '
                  'I''ll consider doing it\n', ngen)
            print('Please provide an integer, stupid!\n')
            return

        # curgen=length(mlc.population);
        curgen = 0
        if curgen == 0:
            # population is empty, we have to create it
            curgen = 1
            self.generate_population(curgen)
            # self.eng.generate_population(self.mlc) #mlc.generate_population;

        while curgen <= ngen:
            # ok we can do something
            state = self.eng.get_population_state(self.mlc, curgen)
            if state == 'init':
                if curgen == 1:
                    self.generate_population(curgen)
                    # self.eng.generate_population(self.mlc)
                else:
                    self.evolve_population()
                    # self.eng.evolve_population(self.mlc)

            elif state == 'created':
                self.eng.evaluate_population(self.mlc)

            elif state == 'evaluated':
                curgen += 1

                if fig > 0:
                    self.eng.show_best(self.mlc)

                # if (fig>1):
                    # self.eng.show_convergence(self.mlc)

                if curgen <= ngen:
                    self.evolve_population()
                    # self.eng.evolve_population(self.mlc)

    def generate_population(self, gen_number):
        population = self.eng.MLCpop(self.params)
        self.eng.workspace["wpopulation"] = population
        print self.eng.eval("wpopulation.state")

        self.eng.create(population, self.params, self.table)
        self.eng.set_state(population, 'created')
        print self.eng.eval("wpopulation.state")

        self.eng.add_population(self.mlc, population, gen_number)

        # mlc.population=MLCpop(mlc.parameters);
        # [mlc.population(1),mlc.table]=mlc.population.create(mlc.parameters);

    def evolve_population(self):
        n = self.eng.get_current_generation(self.mlc)
        current_pop = self.eng.get_population(self.mlc, n)

        next_pop = self.eng.MLCpop(self.params)
        self.eng.evolve(current_pop, self.params, self.table, next_pop)

        self.eng.set_state(next_pop, 'created')
        self.eng.add_population(self.mlc, next_pop, n+1)

        '''
        self.eng.workspace["wparams"] = self.params
        if (self.eng.eval("wparams.lookforduplicates")):
            self.eng.remove_duplicates(next_pop)
            %% Remove duplicates

        if mlc.parameters.lookforduplicates
            mlc.population(n+1).remove_duplicates;
            idx=find(mlc.population(n+1).individuals==-1);
            while ~isempty(idx);
                [mlc.population(n+1),mlc.table]=mlc.population(n).evolve(mlc.parameters,mlc.table,mlc.population(n+1));
                mlc.population(n+1).remove_duplicates;
                idx=find(mlc.population(n+1).individuals==-1);
            end
        end
        mlc.population(n+1).state='created';
        '''