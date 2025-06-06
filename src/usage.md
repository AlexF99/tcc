## Metanome

### Pyro
	java -cp metanome-cli-1.1.0.jar:../algorithms/pyro-distro-1.0-SNAPSHOT-distro.jar de.metanome.cli.App --algorithm de.hpi.isg.pyro.algorithms.Pyro \
	--files ../datasets/adult.csv \
	--file-key inputFile \
	--separator "," \
	--algorithm-config isFindKeys:false \
	--algorithm-config isFindFds:true
	
	Obs: POSSÍVEL parâmetro que define error threshold
	--algorithm-config maxUccError:0 errDev:0

### HyFD
	java -cp metanome-cli-1.1.0.jar:../algorithms/HyFD-1.2-SNAPSHOT.jar de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD \
	--files ../datasets/adult.csv \
	--file-key INPUT_GENERATOR \
	--separator ","


Obs:
 - Cada algoritmo possui um --file-key diferente - precisa ver no código qual é

run.sh
 - É possível rodar o pyro para diferentes thresholds colocando a flag pyro-threshold, ex: ./run.sh pyro-threshold 



## FDX
	cd fastApi
	sudo docker compose build
	sudo docker compose up
	hit POST endpoint localhost:8000/profile-file with file and parameters
	example with requests lib:
	```
	url = "http://localhost:8000/profile-file/"
	files = {"file": open(file_path, "rb")}
	form_data = {
		"na_values": self.na_values,
		"sparsity": self.sparsity
	}
	response = requests.post(
		url, 
		files=files, 
		params=form_data
	)

	fds = response.json()['fds']
	dataset_name = response.json()['dataset_name']
	```
