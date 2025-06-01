package <%= projectNameSnake.downcase %>.engine.services;

import <%= projectNameSnake.downcase %>.engine.dtos.NamedId;
import <%= projectNameSnake.downcase %>.engine.dtos.Lookups;
import <%= projectNameSnake.downcase %>.engine.utilities.EnumUtils;

import java.util.List;

public class LookupsService {

	public Lookups getLookups() {
		var lookups = new Lookups();

		return lookups;
	}

}