package <%= projectNameSnake.downcase %>.app;

import <%= projectNameSnake.downcase %>.engine.services.LookupsService;

import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@Component
class AppDependencies {

	@Bean
	public LookupsService getLookupsService() {
		return new LookupsService();
	}
}