"""
Factory class to create agent interface objects 
given the agent type passed in.
"""
from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_factory.verifier_agent_interface import VerifierAgentInterface
from agent_factory.holder_agent_interface import HolderAgentInterface
from agent_factory.aath.aath_issuer_agent_interface import AATHIssuerAgentInterface
from agent_factory.aath.aath_verifier_agent_interface import AATHVerifierAgentInterface
from agent_factory.aath.aath_holder_agent_interface import AATHHolderAgentInterface
from agent_factory.candy_uvp.candy_uvp_issuer_agent_interface import CANdy_UVP_IssuerAgentInterface
from agent_factory.bc_person_showcase.bc_person_showcase_verifier_agent_interface import BCPersonShowcaseVerifierAgentInterface
from agent_factory.bc_vp.bc_vp_issuer_agent_interface import BC_VP_IssuerAgentInterface


class AgentInterfaceFactory():
    
    issuer_agent_type_interface_dict = {
        "AATH": AATHIssuerAgentInterface,
        "CANdy_UVP": CANdy_UVP_IssuerAgentInterface,
        "BC_VP": BC_VP_IssuerAgentInterface
    }
    verifier_agent_type_interface_dict = {
        "AATH": AATHVerifierAgentInterface,
        "BC_Person_Showcase": BCPersonShowcaseVerifierAgentInterface
    }
    holder_agent_type_interface_dict = {
        "AATH": AATHHolderAgentInterface
    }
    
    def create_issuer_agent_interface(self, agent_type, agent_endpoint) -> IssuerAgentInterface:
        """create an issuer agent interface object of the type given"""
        return self.issuer_agent_type_interface_dict[agent_type](agent_endpoint)

    def create_verifier_agent_interface(self, agent_type, agent_endpoint) -> VerifierAgentInterface:
        """create a verifier agent interface object of the type given"""
        return self.verifier_agent_type_interface_dict[agent_type](agent_endpoint)
    
    def create_holder_agent_interface(self, agent_type, agent_endpoint) -> HolderAgentInterface:
        """create a holder agent interface object of the type given"""
        return self.holder_agent_type_interface_dict[agent_type](agent_endpoint)